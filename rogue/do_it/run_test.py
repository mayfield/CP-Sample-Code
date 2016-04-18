"""
Do something, one-shot
"""
import os

from cp_lib.app_base import CradlepointAppBase


# this name "run_router_app" is not important, reserved, or demanded
# - but must match below in __main__ and also in __init__.py
def run_router_app(app_base):
    """

    :param CradlepointAppBase app_base: resources: logger, settings, etc
    """

    app_base.logger.info("Running something ... roguish")

    # check_file_list(app_base)
    # probe_directory(app_base, "/usr/lib/python3.3")
    # probe_directory(app_base, "/dev")
    # probe_directory(app_base, "/etc")

    # confirm we can create some files
    do_file_test(app_base)

    return 0


def check_file_list(app_base):
    """
    Check if some files got unpacked okay
    :param CradlepointAppBase app_base: resources: logger, settings, etc
    """
    files = [
        "config/settings.json",
        "cp_lib/app_name_parse.py",
        "cp_lib/clean_ini.py",
        "cp_lib/cp_logging.py",
        "cp_lib/hw_status.py",
        "cp_lib/load_settings.py",
        "cp_lib/split_version.py",
        "install.sh",
        "main.py",
        "package.ini",
        "simple/hello_world/hello_world.py",
        "simple/hello_world/settings.json",
        "start.sh",
    ]

    for name in files:
        test_access(name, app_base)
    return


def test_access(name, app_base):
    result = os.access(name, os.R_OK)
    if result:
        app_base.logger.debug("GOOD file:{}".format(name))
    else:
        app_base.logger.debug("BAD file:{}".format(name))
    return result


def probe_directory(app_base, base_dir):
    """
    Check if some files got unpacked okay
    :param CradlepointAppBase app_base: resources: logger, settings, etc
    :param str base_dir: the directory to dump
    """
    app_base.logger.debug("Dump Directory:{}".format(base_dir))
    result = test_access(base_dir, app_base)
    if result:
        result = os.listdir(base_dir)
        for name in result:
            app_base.logger.debug("  file:{}".format(name))
    return


def do_file_test(app_base):
    app_base.logger.debug("Do File Test")
    app_base.logger.debug("Original base directory")
    probe_directory(app_base, ".")
    make_file(app_base, "test1.csv")
    app_base.logger.debug("After 1st file base directory")
    probe_directory(app_base, ".")

    os.mkdir("data")
    app_base.logger.debug("After MKDIR base directory")
    probe_directory(app_base, ".")

    app_base.logger.debug("After 2nd file base directory")
    make_file(app_base, "data/test2.csv")
    probe_directory(app_base, ".")
    probe_directory(app_base, "data")
    return


def make_file(app_base, file_name):
    """
    Check if some files got unpacked okay
    :param CradlepointAppBase app_base: resources: logger, settings, etc
    :param str file_name: the filename to create
    """
    data = "0,12938,Hello,23\n"
    app_base.logger.debug("Write {} with {}".format(file_name, data))
    file_han = open(file_name, "w")
    file_han.write(data)
    file_han.close()
    return


if __name__ == "__main__":
    import sys

    my_app = CradlepointAppBase("rogue/do_it")

    _result = run_router_app(my_app)
    my_app.logger.info("Exiting, status code is {}".format(_result))
    sys.exit(_result)
