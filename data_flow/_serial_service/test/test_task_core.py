# Test the TASK MASTER module

import unittest
import time

import common.log_module as log_module
from task.task_core import TaskCore


class TestTaskCore(unittest.TestCase):

    def test_basic(self):

        # we start by creating the Task Master
        obj = TaskCore('sammy')
        obj.set_logger_level(log_module.DEBUG)

        self.assertEqual(obj['state'], obj.STATE_INIT)
        self.assertEqual(obj['last_activity'], 0.0)
        with self.assertRaises(KeyError):
            if obj['health']:
                pass

        now = time.time()
        obj.touch(now)
        self.assertEqual(obj['last_activity'], now)

        obj.allocate(now)
        self.assertEqual(obj['state'], obj.STATE_ALLOC)

        health = obj['health']
        print(health._attrib)
        health_sample = obj['health']['value']
        # self.assertEqual(obj['health'].get_value(), obj.HEALTH_ALLOC)
        self.assertEqual(health_sample.get_value(), obj.HEALTH_ALLOC)

        return


if __name__ == '__main__':

    unittest.main()
