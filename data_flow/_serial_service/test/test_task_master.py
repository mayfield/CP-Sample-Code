# Test the TASK MASTER module

import unittest
import time

from common.log_module import LogWrapper
from data.cp_api import ApiRouterDisk
import data.data_base as data_base
from task.get_task_master import get_task_master
# from task.task_master import TaskMaster
from task.task_time import TimeMaster


class TestTaskMaster(unittest.TestCase):

    def test_basic(self):

        # we start by creating the Task Master
        task_master = get_task_master()

        time_master = TimeMaster()

        now = time.time()
        task_master.allocate(now)

        data_base.print_base_report(task_master.database)

        # # zero is special, as it is not relevant to this function
        # seconds = 0
        # self.assertFalse(time_period.is_valid_clean_period_seconds(seconds))
        # # self.assertFalse((60 % seconds) == 0)
        #
        # # one is typical TRUE situation - see '7' for typical FALSE situation
        # seconds += 1  # == 1
        # self.assertTrue(time_period.is_valid_clean_period_seconds(seconds))
        # self.assertTrue((60 % seconds) == 0)
        #
        # with self.assertRaises(ValueError):
        #     time_period.is_valid_clean_period_seconds('7.1')

        return


def build_api_tree():

    logger = LogWrapper("build_api")
    logger.setLevel('DEBUG')

    api = ApiRouterDisk()

    # confirm the basic config tree is there
    paths = [
        "config/task/",
        "config/task/taskmaster/",
        "config/task/timemaster/",
        "status/task/",
        "status/task/taskmaster/",
        "status/task/timemaster/",
    ]
    for path in paths:
        message = "Confirm path \"{0}\"".format(path)
        logger.info(message)
        api.verify_exists(path)

    return


if __name__ == '__main__':

    if True:
        unittest.main()
    else:
        build_api_tree()
