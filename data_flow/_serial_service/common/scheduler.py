__author__ = 'LLinse'

import sched
import time


class Scheduler(sched.scheduler):
    """
    A wrapper for the standard Python 3.4 scheduler class
    """

    def __init__(self):
        super().__init__(time.time, time.sleep)
        return

