# File: task.__init__.py
# Desc: the base class (TaskCore) for the TASK objects, plus the TaskMaster. This is unrelated to
#       threads or Threading, but is a handle to allow the 'app' to manage its sub-parts

import threading
import time

import data.data_object as data_object

__version__ = "1.0.1"

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
# 1.0.1: 2015-Dec Lynn
#       * propagate time better
#

# how fast all threads/modules are expected to comply with a shutdown request. This primarily
# means no thread should block longer than this time, so that they can check for shutdown event
TASK_SHUTDOWN_SECONDS = 10


class TaskCore(object):
    """
    Defines a service module, which may have a task or may not. Start up order may vary,
    however the following must be true:

    1) __init__: all TaskCore objects shall have their self.__init__() method run, they shall not
       assume this has occurred before any other TaskCore; order may vary. TaskCore instances must
       NOT do long things (such as external network searches during init!

    2) allocate: all TaskCore objects shall have their self.allocate() method run. These should
       not do any time-variable external tasks. The only thing they can assume is that all TaskCore
       have completed step #1 (__init__). However, references to other TaskCore can be retrieved
       from the TaskMaster, but not specific function beyond that can be assumed. TaskCore
       instances must NOT do long things (such as external network searches during init!

    3) start: after all 'allocate' methods have returned, then each TaskCore is started. They may
       begin longer actions now, however if they do things taking longer than a second, they should
       be using their own thread!

    Attribute of every TaskCore:
    ['name']: str,  unique indexable name
    ['state']: str, state name, such as 'running' or 'fault'
    ['health']: float, is a somewhat arbitrary status between 0% and 100%. All we know is 0% means
        totally broken, and 100% means perfectly functional.
    ['last_activity']: float, is a timestamp, however when viewed externally anything within the
        past one minute is fine, as we'll not refresh always.
    """

    STATE_INIT = 'init'
    STATE_ALLOC = 'allocate'
    STATE_START = 'start'
    STATE_RUNNING = 'running'
    STATE_SHUTDOWN = 'shutdown'
    STATE_FAULT = 'fault'
    STATE_LIST = ('init', 'allocate', 'start', 'running', 'shutdown', 'fault')

    HEALTH_ALLOC = 10.0
    HEALTH_SHUTDOWN = 5.0
    HEALTH_FAULT = 0.0

    API_NAME = None

    STATUS_TASK_NAME = 'status/task/'

    def __init__(self, name):
        """
        Initial Python allocation.

        :param name: an indexable string, unique to this application
        :type name: str
        """

        from common.log_module import LogWrapper
        from data.data_types import validate_name
        from data.cp_api import ApiRouterDisk
        from data.data_base import get_core_database
        from task.get_task_master import get_task_master

        name = validate_name(name)
        self._attrib = dict()
        self._attrib['name'] = name

        # point to our database (will this hide the api?)
        self.database = get_core_database()

        # our object is a collection of our attributes
        self.task_object = data_object.DataObject(self['name'])
        self.task_object.set_attribute('path', self.STATUS_TASK_NAME + self['name'])

        # TaskMaster adds to DB!
        # self.database.add_to_data_base(self.task_object)

        self._attrib['state'] = self.STATE_INIT
        self._attrib['last_activity'] = 0.0

        # this event is used to safely request shutdown in a multi-threaded environment
        self.do_shutdown = threading.Event()

        # each module has it's own logger instance, which allows varying logger output
        # in larger systems.
        self.logger = LogWrapper(name)

        # handle the config and status
        self.api = ApiRouterDisk()
        self.api.verify_exists(self.STATUS_TASK_NAME + self['name'] + '/')
        self.api_put_status('name', self['name'])

        if name != "taskmaster":
            # if there is no task-master, one is created here.
            self.task_master = get_task_master()
            self.database.add_to_data_base(self.task_object)
        pass

    @staticmethod
    def code_name():
        return 'TaskCore'

    @staticmethod
    def code_version():
        return __version__

    def __getitem__(self, key):
        return self._attrib[key]

    def __setitem__(self, key, value):
        self._attrib[key] = value

    def api_put_status(self, name, value):
        """
        Our status
        :param name:
        :param value:
        :return:
        """
        path = self._api_make_path(name)
        self.api.put(path, value)
        return

    def _api_make_path(self, name: str, config=False):
        """
        make the basic API item path, such as "status/task/{my_name}/value_name"
        :param name:
        :rtype: str
        """
        if config:
            path = "config"
        else:
            path = "status"
        path += self.api.SEP + 'task' + self.api.SEP + self['name'] + self.api.SEP + name
        return path

    def set_logger_level(self, level):
        """
        Change the logging for this TaskCore object

        :param level: the level as defined by 'logging' module
        :type level: int or str
        """
        self.logger.setLevel(level)

    def reset(self, now=None):
        """
        return TaskCore to a pre-allocate state. Generally, only TaskMaster calls.
        """
        self.set_state(self.STATE_INIT, now)
        self.set_health(0.0, now)
        return

    def touch(self, now=None):
        """
        Update the time() of last activity

        :param now: the time() stamp to record for the event
        :type now: float
        :return:
        """
        if now is None:
            now = time.time()
        self._attrib['last_activity'] = now
        # handle propagation
        return

    def allocate(self, now):
        """
        The middle-step in startup - allocate all internal resources. All TaskCore objects shall
        complete their 'allocate' method before moving to the start step.

        :param now: the time we started this state
        :type now: float
        :rtype: bool
        """

        self.set_state(self.STATE_ALLOC, now)
        self.do_shutdown.clear()

        # health is a value between 0% and 100%
        self.set_health(self.HEALTH_ALLOC, now)
        return True

    def start(self, now):
        """
        The final-step in startup - begin threads and interaction with external resources.
        TaskCore objects will complete their 'start' method in various times and order.

        :param now: the time we started this state
        :type now: float
        :rtype: bool
        """
        self.set_state(self.STATE_START, now)
        self.set_health(25.0, now)
        return True

    def running(self, now):
        """
        Largely a transition from 'start' to 'running'. change status and do some audit logging.
        set health back to 0%, assuming task updates

        :param now: the time we started this state
        :type now: float
        :rtype: bool
        """
        self.set_state(self.STATE_RUNNING, now)
        return True

    def shutdown(self, now):
        """
        Request the Task to shutdown. Any modules should comply within TASK_SHUTDOWN_SECONDS time.

        :param now: the time we started this state
        :type now: float
        :rtype: bool
        """
        self.set_state(self.STATE_SHUTDOWN, now)
        self.set_health(self.HEALTH_SHUTDOWN, now)
        return True

    def fault(self, now):
        """
        Go into an unrecoverable fault state.

        :param now: the time we started this state
        :type now: float
        :rtype: bool
        """
        self.set_state(self.STATE_FAULT, now)
        self.set_health(self.HEALTH_FAULT, now)
        return True

    def set_health(self, value, now=None):
        """
        Update the attribute, plus propagate as required

        :param value: the health value, between 0 and 100%
        :type value: float
        :param now: the time we started this state
        :type now: float
        """
        if 'health' not in self._attrib:
            # then create the health data object
            path = self.STATUS_TASK_NAME + '{0}/health'.format(self['name'])
            data = data_object.NumericObject('health')
            data.set_attribute('path', path)
            data.set_template(self.database.find_template_object('_health'))
            self.database.add_to_data_base(data)
            self['health'] = data

        if self['health'].set_value(value, now):
            # then changed, so handle the propagation
            self.api_put_status('health', value)
        return

    def set_last_activity(self, value):
        """
        Update the attribute, plus propagate as required

        :param value: the time() of last activity
        :type value: float
        """
        if value is None:
            value = time.time()
        self._attrib['last_activity'] = value
        # handle propagation
        return

    def set_state(self, value, now=None):
        """
        Update the attribute, plus propagate as required

        :param value: the state as string name, such as 'running'
        :type value: str
        :param now: the time we started this state
        :type now: float
        """
        if value not in self.STATE_LIST:
            raise ValueError("Task State bad:{0} - must be in {1}".format(value, self.STATE_LIST))

        self._attrib['state'] = value

        if now is not None:
            # if given a time
            self.touch(now)

        # handle propagation
        self.api_put_status('state', value)
        return
