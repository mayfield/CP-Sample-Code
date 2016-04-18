# File: task_time.py
# Desc: the Time manager - handles future 'timed' callbacks and cyclic callbacks

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Aug Lynn
#       * initial draft
#
#

from common.time_period import TimePeriods
from task.task_core import TaskCore


class TimeMaster(TaskCore):

    API_NAME = 'timemaster'

    def __init__(self, name=None):
        if name is None:
            name = self.code_name()
        super().__init__(name)

        # add our self to our base collection
        self.task_master.add_task(self)

        # this is a thread object, but do not start yet
        self.my_thread = TimePeriods()
        self.my_thread.logger = self.logger
        return

    @staticmethod
    def code_name():
        return 'TimeMaster'

    @staticmethod
    def code_version():
        return __version__

    def reset(self, now=None):
        """
        return TaskCore to a pre-allocate state. Generally, only TaskMaster calls.
        """
        return

    def allocate(self, now: float):
        """
        For Time Master, this means insure all of our sub tasks enter and complete allocate.

        :rtype: bool
        """
        super().allocate(now)

        # this will cause new thread to be created, and TimePeriod.run() to be called
        self.logger.debug("Starting Thread")
        self.my_thread.start()
        return True

    # use super().start(now)

    def running(self, now: float):
        """
        Largely a transition from 'start' to 'running'. change status and do some audit logging.
        set health back to 0%, assuming task updates

        :rtype: bool
        """
        super().start(now)
        self.set_health(100.0, now)
        self.my_thread.add_periodic_callback(cb=self._per_minute_refresh, period="1 min")

        return True

    def shutdown(self, now: float):
        """
        Request the Task to shutdown. Any modules should comply within TASKThe final-step in
        startup - begin threads and interaction with external resources.
        TaskCore objects will complete their 'start' method in various times and order.

        :rtype: bool
        """
        super().shutdown(now)
        self.my_thread.shutdown_requested.set()
        return True

    # use super().fault(now), but really should arrange total shutdown!

    def _per_minute_refresh(self, now_tuple):
        """
        Once per minute, we update out LAST ACTIVITY

        :param now_tuple:
        :return:
        """
        if now_tuple:
            pass

        self.set_last_activity(self.my_thread.now)
        return
