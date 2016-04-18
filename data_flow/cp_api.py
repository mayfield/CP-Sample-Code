import os
import os.path
import json

from common.log_module import LogWrapper

if os.path.isdir("C:/Users/Lynn"):
    API_BASE_PATH = "C:/Users/Lynn/Box Sync/serial_service/"
elif os.path.isdir("C:/Users/llinse"):
    API_BASE_PATH = "C:/Users/llinse/Box Sync/serial_service/"
else:
    API_BASE_PATH = None


class ApiRouter(object):

    DATA_NAME = "store.json"
    DATA_SUFFIX = ".json"

    # windows allows either type
    SEP = '/'

    # if true, pokes the subdirectory name into the store.json file
    SAVE_PATH = True

    def __init__(self):
        self.mode = 'disk'

        # if os.path.isdir('api'):
        #     # then we do NOT need this hack for unittests
        #     self.BASE_PATH = None
        # self.cwd = os.getcwd()
        # TODO - handle diverse paths?

        self.logger = LogWrapper("router_api")
        self.logger.setLevel("INFO")
        # self.logger.setLevel("DEBUG")
        return

    def get(self, path):
        """
        Given an API string, fetch the value as native Python

        :param path:
        :type path: str
        :return:
        """
        if not isinstance(path, str):
            raise TypeError("get PATH must be type str")

        if not path.startswith("api"):
            path = "api" + path

        return path

    def put(self, path, value):
        if not isinstance(path, str):
            raise TypeError("get PATH must be type str")

        if not path.startswith("api"):
            path = "api" + path

        return path

    def _validate_path(self, path):
        if not isinstance(path, str):
            raise TypeError("get PATH must be type str")

        # print("path({0})".format(path))
        if not path.startswith("api"):
            if len(path) and path[0] != self.SEP:
                path = "api" + self.SEP + path
            else:
                path = "api" + path

        if API_BASE_PATH is not None:
            path = API_BASE_PATH + path

        return path


class ApiRouterDisk(ApiRouter):

    def __init__(self):
        ApiRouter.__init__(self)
        self.mode = 'disk'
        return

    def get(self, path):
        """
        Given an API string, fetch the value as native Python

        :param path:
        :type path: str
        :return:
        """
        # print('    get({})'.format(path))
        path = self._validate_path(path)

        if os.path.isdir(path):
            # if path exists as a directory

            data = dict()

            dir_list = os.listdir(path)
            for name in dir_list:
                if name == self.DATA_NAME:
                    # then open the store.json, just put into the 'root'
                    data.update(self._get_or_create(path))

                else:  # recurse into the subdirectory
                    data.update(self._get_sdir(path, name))

        else:  # assume is something inside "store.json"
            data = self._get_value(path)

        return data

    def _get_sdir(self, path, sub_name):
        """
        Given an API string, fetch the value as native Python

        :param path:
        :type path: str
        :return:
        """
        self.logger.debug('_get_sdir({0}, {1})'.format(path, sub_name))
        sub_path = path + self.SEP + sub_name
        data = {}

        dir_list = os.listdir(sub_path)
        for name in dir_list:
            if name == self.DATA_NAME:
                # then open the store.json, just put into the 'root'
                sub_data = self._get_store(sub_path)
                if sub_data is not None:
                    data.update(sub_data)

            else:  # recurse into the subdirectory
                data.update(self._get_sdir(sub_path, name))

        return {sub_name: data}

    def _get_store(self, path):
        """
        Assume path_value has a desired value in 'tail'

        :param path:
        :type path: str
        :return:
        """
        # print('    _get_store({0})'.format(path))
        data = self._get_or_create(path)
        if data == {}:
            data = None
        return data

    def _get_value(self, path_value):
        """
        Assume path_value has a desired value in 'tail'

        For example: api.get("/config/serial/0/mode"),
                     where "/config/serial/0" = {"mode": "tcp"}
                     so the return value is "tcp"

        :param path_value:
        :type path_value: str
        :return:
        """
        # print('    _get_value({0})'.format(path_value))
        path, value = os.path.split(path_value)
        data = self._get_or_create(path)
        if value in data:
            data = data[value]
        else:
            data = None

        return data

    def put(self, path, value):
        path = self._validate_path(path)

        if os.path.isdir(path):
            # if path exists as a directory, then insure value is a full dictionary
            if not isinstance(value, dict):
                raise TypeError("put DATA must be type dict")
            self._put_full_data(path, value)
            data = value

        else:  # else we fetch existing store.json, merge in value and save again
            head, tail = os.path.split(path)
            data = self._get_or_create(head)
            data[tail] = value
            self._put_full_data(head, data)

        return True

    def _get_or_create(self, path):

        if not path.endswith(self.DATA_SUFFIX):
            path += self.SEP + self.DATA_NAME

        # print("PWD={0}".format(os.getcwd()))

        try:
            self.logger.debug("Read file:{0}".format(path))
            data_file = open(path, 'r')
            try:
                data = json.load(data_file)
            except ValueError:
                # then data is file is bad
                self.logger.error("bad data in file:{0}".format(path))
                data = {}
            data_file.close()

        except FileNotFoundError:
            data = dict()
            self._put_full_data(path, data)
            self.logger.debug("Created file:{0}".format(path))

        return data

    def _put_full_data(self, path, data):
        """
        Given a
        :param path: the full path to the subdirectory (or the store file). So either of these is okay
                     ("/config/serial", "/config/serial/store.json")
        :type path: str
        :param data:
        :type data: dict
        :return:
        """
        if not isinstance(data, dict):
            raise TypeError("put DATA must be type dict")

        if self.SAVE_PATH:
            data['_path'] = path

        if not path.endswith(self.DATA_SUFFIX):
            path += self.SEP + self.DATA_NAME

        data_file = open(path, 'w')
        data_file.write(json.dumps(data))
        data_file.close()
        return

    def verify_exists(self, path: str):
        return self._make_path(path)

    def _make_path(self, path: str):
        """
        Assume path passed in is to a data item, so we want to make sure the path exists up to,
        but NOT including the final data name.

        For example, if path "/config/serial/0/mode", then make sure:
        1) subdirectory "api/config" exists
        2) subdirectory "api/config/serial" exists
        3) subdirectory "api/config/serial/0" exists
        4) but we assume "mode" is a data item, so do NOT create such a directory

        If the path starts with SEP, the result[0] is ""

        :param path:
        :return:
        """

        # Path:/config/serial/0/mode (starts with SEP causes blank [0])
        # [0] = ""
        # [1] = "config"
        # [2] = "serial"
        # [3] = "0"
        # [4] = "mode"  (we pop this off the list, assume "mode" is data value NOT a directory)
        #
        # Path:config/serial/0/mode
        # [0] = "config"
        # [1] = "serial"
        # [2] = "0"
        # [3] = "mode"  (we pop this off the list, assume "mode" is data value NOT a directory)
        #
        # Path:config/serial/0/mode/ (end with SEP causes blank [-1])
        # [0] = "config"
        # [1] = "serial"
        # [2] = "0"
        # [3] = "mode"
        # [4] = ""  (we pop this off the list, assume "mode" is directory)

        path_parts = path.split(self.SEP)
        if len(path_parts) > 1:
            # pop off the last item, which might be "" or the data value
            path_parts.pop(-1)

        work_path = self._validate_path("")
        # print("work1:(%s)" % work_path)

        # print("cwd:(%s)" % os.getcwd())

        count = 0
        for x in path_parts:
            # print("x1:(%s)" % x)
            if work_path[-1] != self.SEP:
                work_path += self.SEP
            work_path += x
            if not os.path.isdir(work_path):
                # os.mkdir(work_path)
                os.makedirs(work_path, exist_ok=True)
                count += 1
                self.logger.debug("Mkdir:{0}".format(work_path))

        return count
