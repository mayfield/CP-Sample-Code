# Test the cp_lib.app_base module

import logging
import os
import unittest


class TestAppBase(unittest.TestCase):

    def test_import_full_file_name(self):
        """
        :return:
        """
        from cp_lib.app_base import CradlepointAppBase

        print()  # move past the '.'

        if True:
            return

        name = "network.tcp_echo"
        obj = CradlepointAppBase(name)

        # here, the INIT is used, it exists and is larger than trivial (5 bytes)
        # we want the tcp-echo.py to exist, but won't use
        expect = os.path.join("network", "tcp_echo", "tcp_echo.py")
        self.assertTrue(os.path.exists(expect))

        expect = os.path.join("network", "tcp_echo", "__init__.py")
        self.assertTrue(os.path.exists(expect))
        logging.info("TEST names when {} can be run_name".format(expect))

        self.assertEqual(obj.run_name, expect)
        expect = os.path.join("network", "tcp_echo") + os.sep
        self.assertEqual(obj.app_path, expect)
        self.assertEqual(obj.app_name, "tcp_echo")
        self.assertEqual(obj.mod_name, "network.tcp_echo")

        name = "RouterSDKDemo"
        obj = CradlepointAppBase(name)

        # here, the app name is used (the INIT is empty / zero bytes)
        expect = os.path.join("RouterSDKDemo", "__init__.py")
        self.assertTrue(os.path.exists(expect))
        logging.info("TEST names when {} is too small to be run_name".format(expect))

        expect = os.path.join(name, name) + ".py"
        self.assertTrue(os.path.exists(expect))
        logging.info("TEST names when {} can be run_name".format(expect))

        self.assertEqual(obj.run_name, expect)
        expect = name + os.sep
        self.assertEqual(obj.app_path, expect)
        self.assertEqual(obj.app_name, "RouterSDKDemo")
        self.assertEqual(obj.mod_name, "RouterSDKDemo")

        return

    def test_normalize_app_name(self):
        """
        :return:
        """
        from cp_lib.app_name_parse import normalize_app_name, get_module_name, get_app_name, \
            get_app_path
        # TODO - test get_run_name()!
        import os

        print()  # move past the '.'

        logging.info("TEST normalize_app_name()")
        tests = [
            ("network\\tcp_echo\\file.py", ["network", "tcp_echo", "file.py"]),
            ("network\\tcp_echo\\file", ["network", "tcp_echo", "file", ""]),
            ("network\\tcp_echo\\", ["network", "tcp_echo", ""]),
            ("network\\tcp_echo", ["network", "tcp_echo", ""]),

            ("network/tcp_echo/file.py", ["network", "tcp_echo", "file.py"]),
            ("network/tcp_echo/file", ["network", "tcp_echo", "file", ""]),
            ("network/tcp_echo/", ["network", "tcp_echo", ""]),
            ("network/tcp_echo", ["network", "tcp_echo", ""]),

            ("network.tcp_echo.file.py", ["network", "tcp_echo", "file.py"]),
            ("network.tcp_echo.file", ["network", "tcp_echo", "file", ""]),
            ("network.tcp_echo.", ["network", "tcp_echo", ""]),
            ("network.tcp_echo", ["network", "tcp_echo", ""]),

            ("network", ["network", ""]),
            ("network.py", ["", "network.py"]),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = normalize_app_name(source)
            # logging.debug("normalize_app_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.info("TEST get_module_name()")
        tests = [
            ("network\\tcp_echo\\file.py", "network.tcp_echo"),
            ("network\\tcp_echo\\file", "network.tcp_echo.file"),
            ("network\\tcp_echo", "network.tcp_echo"),

            ("network/tcp_echo/file.py", "network.tcp_echo"),
            ("network/tcp_echo/file", "network.tcp_echo.file"),
            ("network/tcp_echo", "network.tcp_echo"),

            ("network.tcp_echo.file.py", "network.tcp_echo"),
            ("network.tcp_echo.file", "network.tcp_echo.file"),
            ("network.tcp_echo", "network.tcp_echo"),

            ("network", "network"),
            ("network.py", ""),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = get_module_name(source)
            # logging.debug("get_module_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.info("TEST get_app_name()")
        tests = [
            ("network\\tcp_echo\\file.py", "tcp_echo"),
            ("network\\tcp_echo\\file", "file"),
            ("network\\tcp_echo", "tcp_echo"),

            ("network/tcp_echo/file.py", "tcp_echo"),
            ("network/tcp_echo/file", "file"),
            ("network/tcp_echo", "tcp_echo"),

            ("network.tcp_echo.file.py", "tcp_echo"),
            ("network.tcp_echo.file", "file"),
            ("network.tcp_echo", "tcp_echo"),

            ("network", "network"),
            ("network.py", ""),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = get_app_name(source)
            # logging.debug("get_app_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.info("TEST get_app_path(), with native os.sep, which = \'{}\'".format(os.sep))
        tests = [
            ("network\\tcp_echo\\file.py", os.path.join("network", "tcp_echo") + os.sep),
            ("network\\tcp_echo\\file", os.path.join("network", "tcp_echo", "file") + os.sep),
            ("network\\tcp_echo", os.path.join("network", "tcp_echo") + os.sep),

            ("network/tcp_echo/file.py", os.path.join("network", "tcp_echo") + os.sep),
            ("network/tcp_echo/file", os.path.join("network", "tcp_echo", "file") + os.sep),
            ("network/tcp_echo", os.path.join("network", "tcp_echo") + os.sep),

            ("network.tcp_echo.file.py", os.path.join("network", "tcp_echo") + os.sep),
            ("network.tcp_echo.file", os.path.join("network", "tcp_echo", "file") + os.sep),
            ("network.tcp_echo", os.path.join("network", "tcp_echo") + os.sep),

            ("network", "network" + os.sep),
            ("network.py", ""),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = get_app_path(source)
            # logging.debug("get_module_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.info("TEST get_app_path(), with forced LINUX separator of \'/\'")
        tests = [
            ("network\\tcp_echo\\file.py", "network/tcp_echo/"),
            ("network\\tcp_echo\\file", "network/tcp_echo/file/"),
            ("network\\tcp_echo", "network/tcp_echo/"),

            ("network/tcp_echo/file.py", "network/tcp_echo/"),
            ("network/tcp_echo/file", "network/tcp_echo/file/"),
            ("network/tcp_echo", "network/tcp_echo/"),

            ("network.tcp_echo.file.py", "network/tcp_echo/"),
            ("network.tcp_echo.file", "network/tcp_echo/file/"),
            ("network.tcp_echo", "network/tcp_echo/"),

            ("network", "network/"),
            ("network.py", ""),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = get_app_path(source, separator='/')
            # logging.debug("get_module_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.info("TEST get_app_path(), with forced WINDOWS separator of \'\\\'")
        tests = [
            ("network\\tcp_echo\\file.py", "network\\tcp_echo\\"),
            ("network\\tcp_echo\\file", "network\\tcp_echo\\file\\"),
            ("network\\tcp_echo", "network\\tcp_echo\\"),

            ("network/tcp_echo/file.py", "network\\tcp_echo\\"),
            ("network/tcp_echo/file", "network\\tcp_echo\\file\\"),
            ("network/tcp_echo", "network\\tcp_echo\\"),

            ("network.tcp_echo.file.py", "network\\tcp_echo\\"),
            ("network.tcp_echo.file", "network\\tcp_echo\\file\\"),
            ("network.tcp_echo", "network\\tcp_echo\\"),

            ("network", "network\\"),
            ("network.py", ""),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = get_app_path(source, separator='\\')
            # logging.debug("get_module_name({0}) = {1}".format(source, result))

            self.assertEqual(result, expect)

        logging.warning("TODO - we don't TEST get_run_name()")

        return

    def test_normalize_path_separator(self):
        """
        :return:
        """
        from cp_lib.app_name_parse import normalize_path_separator
        import os

        print()  # move past the '.'

        logging.info("TEST normalize_path_separator() to Windows Style")
        tests = [
            ("network\\tcp_echo\\file.py", "network\\tcp_echo\\file.py"),
            ("network\\tcp_echo\\file", "network\\tcp_echo\\file"),
            ("network\\tcp_echo", "network\\tcp_echo"),

            ("network\\tcp_echo/file.py", "network\\tcp_echo\\file.py"),

            ("network/tcp_echo/file.py", "network\\tcp_echo\\file.py"),
            ("network/tcp_echo/file", "network\\tcp_echo\\file"),
            ("network/tcp_echo", "network\\tcp_echo"),

            ("network.tcp_echo.file.py", "network.tcp_echo.file.py"),

            ("network", "network"),
            ("network.py", "network.py"),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = normalize_path_separator(source, separator="\\")
            # logging.debug("normalize_path_separator({0}) = {1}".format(source, result))
            self.assertEqual(result, expect)

        logging.info("TEST normalize_path_separator() to Linux Style")
        tests = [
            ("network\\tcp_echo\\file.py", "network/tcp_echo/file.py"),
            ("network\\tcp_echo\\file", "network/tcp_echo/file"),
            ("network\\tcp_echo", "network/tcp_echo"),

            ("network\\tcp_echo/file", "network/tcp_echo/file"),

            ("network/tcp_echo/file.py", "network/tcp_echo/file.py"),
            ("network/tcp_echo/file", "network/tcp_echo/file"),
            ("network/tcp_echo", "network/tcp_echo"),

            ("network.tcp_echo.file.py", "network.tcp_echo.file.py"),

            ("network", "network"),
            ("network.py", "network.py"),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = normalize_path_separator(source, separator="/")
            # logging.debug("normalize_path_separator({0}) = {1}".format(source, result))
            self.assertEqual(result, expect)

        logging.info("TEST normalize_path_separator(), with native os.sep, which = \'{}\'".format(os.sep))
        tests = [
            ("network\\tcp_echo\\file.py", os.path.join("network", "tcp_echo", "file.py")),
            ("network\\tcp_echo\\file", os.path.join("network", "tcp_echo", "file")),
            ("network\\tcp_echo", os.path.join("network", "tcp_echo")),

            ("network\\tcp_echo/file.py", os.path.join("network", "tcp_echo", "file.py")),

            ("network/tcp_echo/file.py", os.path.join("network", "tcp_echo", "file.py")),
            ("network/tcp_echo/file", os.path.join("network", "tcp_echo", "file")),
            ("network/tcp_echo", os.path.join("network", "tcp_echo")),

            ("network.tcp_echo.file.py", "network.tcp_echo.file.py"),

            ("network", "network"),
            ("network.py", "network.py"),
        ]

        for test in tests:
            source = test[0]
            expect = test[1]

            result = normalize_path_separator(source)
            # logging.debug("normalize_path_separator({0}) = {1}".format(source, result))
            self.assertEqual(result, expect)

        return

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
