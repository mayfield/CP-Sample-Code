import data.data_object as data_object
from task.task_core import TaskCore

# File: task_master.py
# Desc: the Task manager - holds a list of tasks, starting/stopping them

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Aug Lynn
#       * initial draft
#
#


class TaskMaster(TaskCore):

    API_NAME = 'taskmaster'

    def __init__(self, name=None):
        if name is None:
            name = "TaskMaster"
        super().__init__(name)

        self.task_list = []

        self.set_active_task(None)

        # confirm the task collection objects exists
        path = 'task'
        self.task_master_object = data_object.DataObject(path)
        self.task_master_object.set_attribute('path', path)
        self.database.add_to_data_base(self.task_master_object)

        # add our self to our base collection
        self.task_master_object.add_child(self.task_object)
        return

    def add_task(self, task):
        """
        Add a task to the lists

        :param task: the TaskCore instance to add
        :type task: TaskCore
        """
        if task in self.task_list:
            # each named task can only be in the list once, so remove and allow to be reappended
            self.logger.warning("Task({0}) was already added!".format(task['name']))
            self.remove_task(task)

        self.logger.debug("Add Task({0})".format(task['name']))

        # this is a list of the actual tasks
        self.task_list.append(task)

        # this is a list of the data objects
        self.task_master_object.add_child(task.task_object)

        task.reset()
        return

    def remove_task(self, task):
        """
        remove a task to the list

        :param task: the TaskCore instance to add
        :type task: TaskCore
        """
        if task in self.task_list:
            self.logger.debug("Remove Task({0})".format(task['name']))
            self.task_list.remove(task)
            # self.task_master_object.remove_child(task)
        return

    def reset(self, now=None):
        """
        return TaskCore to a pre-allocate state. Generally, only TaskMaster calls.
        """
        raise NotImplementedError("TaskMaster cannot be RESET")

    def allocate(self, now):
        """
        For Task Master, this means insure all of our sub tasks enter and complete allocate.

        :param now: the time of the state change
        :type now: float
        :rtype: bool
        """
        super().allocate(now)

        for task in self.task_list:
            self._one_task_allocate(task, now)

        self.logger.debug("Completed Allocate Step")
        return True

    def start(self, now):
        """
        The final-step in startup - begin threads and interaction with external resources.
        TaskCore objects will complete their 'start' method in various times and order.

        :param now: the time of the state change
        :type now: float
        :rtype: bool
        """
        super().start(now)

        for task in self.task_list:
            # this both starts and sets to running
            self._one_task_start(task, now)

        self.logger.debug("Completed Start Step")
        return True

    # def running(self, now):
    #     """
    #     Largely a transition from 'start' to 'running'. change status and do some audit logging.
    #     set health back to 0%, assuming task updates
    #
    #     :param now: the time of the state change
    #     :type now: float
    #     :rtype: bool
    #     """
    #     super().start(now)
    #     return True

    def shutdown(self, now):
        """
        Request the Task to shutdown. Any modules should comply within TASKThe final-step in
        startup - begin threads and interaction with external resources.
        TaskCore objects will complete their 'start' method in various times and order.

        :param now: the time of the state change
        :type now: float
        :rtype: bool
        """
        for task in self.task_list:
            self._one_task_shutdown(task, now)

        super().shutdown(now)
        return True

    def fault(self, now):
        """
        Go into an unrecoverable fault state.

        :param now: the time of the state change
        :type now: float
        :rtype: bool
        """
        for task in self.task_list:
            self._one_task_fault(task, now)

        super().fault(now)
        return True

    def _one_task_allocate(self, task, now):
        """
        Ask one task to complete 'allocate()'

        :param task: the task instance to start
        :type task: TaskCore
        :param now: the time we started the state
        :type now: float
        """
        self.set_active_task(task['name'])
        try:
            task.allocate(now)
            self.set_active_task(None)
            return True

        except Exception as err:
            self.logger.error("_one_task_allocate_failed:{0}".format(err))
            task.fault(now)
            return False

    def _one_task_start(self, task, now):
        """
        Ask one task to complete 'start()', then set to Running when done

        :param task: the task instance to start
        :type task: TaskCore
        :param now: the time we started the state
        :type now: float
        """
        self.set_active_task(task['name'])
        try:
            task.start(now)
            task.running(now)
            self.set_active_task(None)
            return True

        except Exception as err:
            self.logger.error("_one_task_start:{0}".format(err))
            task.fault(now)
            return False

    def _one_task_shutdown(self, task, now):
        """
        Ask one task to shutdown()

        :param task: the task instance to shutdown
        :type task: TaskCore
        :param now: the time we started the state
        :type now: float
        """
        try:
            task.shutdown(now)
            return True

        except Exception as err:
            self.logger.error("_one_task_shutdown:{0}".format(err))
            task.fault(now)
            return False

    def _one_task_fault(self, task, now):
        """
        Ask one task to go to fault

        :param task: the task instance to start
        :type task: TaskCore
        :param now: the time we started the state
        :type now: float
        """
        try:
            task.fault(now)
            return True

        except Exception as err:
            self.logger.error("_one_task_fault:{0}".format(err))
            # task.fault(now)
            return False

    def set_active_task(self, value):
        """
        Update the attribute, plus propagate as required

        :param value: the task name
        :type value: str or None
        """
        if value is None:
            value = "None"
        self._attrib['active_task'] = value
        # handle propagation
        return
