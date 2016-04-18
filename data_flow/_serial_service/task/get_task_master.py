# File: get_task_master.py
# Desc: alloc a global Task manager - holds a list of tasks, starting/stopping them

_task_master = None


def get_task_master():
    global _task_master

    if _task_master is None:
        from task.task_master import TaskMaster

        _task_master = TaskMaster()

    return _task_master
