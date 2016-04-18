
import base64
import requests
from requests.auth import HTTPDigestAuth


class WiPipeHandler(object):

    API_SEP = '/'
    API_TAG = 'api'
    API_BASE = '/api/'
    API_RAW_BASE = 'api/'

    # if T, then we are running on router?
    LOCALHOST_DEFAULT = False

    def __init__(self):

        # if sys.platform == 'win32':
        #     # for Windows,
        self.localhost = self.LOCALHOST_DEFAULT

        self._user_name = None
        self._password = None
        self._address = None
        self._port = 80

        self.url = None
        self._headers = None

        self.trace = None

        return

    def get_topic(self, topic):
        """

        :param topic: the api element path, such as "status/gpio"
        :type topic: str
        :return:
        """

        if self.url is None:
            self._make_url()

        get_url = self.url + self._normalize_path(topic)
        # get_url = self._normalize_path(topic, add_base=True)
        # get_url = "http://192.168.1.1/api/status/gpio"

        # data = requests.get(get_url)
        data = requests.get(get_url, auth=HTTPDigestAuth(self._user_name, self._password))

        if self.trace is not None:
            # url [http://192.168.1.1/api/status/gpio]
            print("url [{}]".format(get_url))

            # data[<Response [200]>]
            print("data[{}]".format(data))

            # json[{'success': False, 'reason': 'authentication failure'}]
            print("json[{}]".format(data.json()))

            # head[{'Transfer-Encoding': 'chunked', 'Date': 'Wed, 03 Feb 2016 19:33:31 GMT',
            #       'Server': 'CradlepointHTTPService/1.0.0', 'Content-Type': 'application/json'}]
            print("head[{}]".format(data.headers))

            # stat[400]
            print("stat[{}]".format(data.status_code))

            # auth_handler = urllib.HTTP()
            #
            # conn = HTTPConnection(self.ADDRESS)
            # conn.set_debuglevel(level=9)
            # conn.connect()
            # # conn.request("GET", get_url, headers=self._headers)
            # conn.request("GET", get_url)
            # response = conn.getresponse()
            # data = response.read()
            # print("data[%s]" % str(data))
            # heads = response.getheader("Www-Authenticate")
            # print("head[%s]" % str(heads))
            # conn.close()

        if 20 <= data.status_code <= 300:
            # then was okay
            return data.json()['data']

        return None

    def put_topic(self, topic, value):
        """

        :param topic: the api element path, such as "status/gpio"
        :type topic: str
        :param value: the data to write
        :return:
        """

        if self.url is None:
            self._make_url()

        get_url = self.url + self._normalize_path(topic)

        data = requests.put(get_url, data={'data': value}, auth=HTTPDigestAuth(self._user_name, self._password))

        if self.trace is not None:
            # url [http://192.168.1.1/api/status/gpio]
            print("url [{}]".format(get_url))

            # data[<Response [200]>]
            print("data[{}]".format(data))

            # json[{'success': False, 'reason': 'authentication failure'}]
            print("json[{}]".format(data.json()))

            # head[{'Transfer-Encoding': 'chunked', 'Date': 'Wed, 03 Feb 2016 19:33:31 GMT',
            #       'Server': 'CradlepointHTTPService/1.0.0', 'Content-Type': 'application/json'}]
            print("head[{}]".format(data.headers))

            # stat[400]
            print("stat[{}]".format(data.status_code))

            # auth_handler = urllib.HTTP()
            #
            # conn = HTTPConnection(self.ADDRESS)
            # conn.set_debuglevel(level=9)
            # conn.connect()
            # # conn.request("GET", get_url, headers=self._headers)
            # conn.request("GET", get_url)
            # response = conn.getresponse()
            # data = response.read()
            # print("data[%s]" % str(data))
            # heads = response.getheader("Www-Authenticate")
            # print("head[%s]" % str(heads))
            # conn.close()

        if 20 <= data.status_code <= 300:
            # then was okay
            return data.json()['data']

        return None

    def set_ip_address(self, value: str):
        """
        Embed the API target name in the handler

        :param value: the intended value to set
        """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError("ip address must be string and not empty")

        self._address = value
        self._make_url()
        return

    def set_password(self, value: str):
        """
        Embed the user password in the handler

        :param value: the intended value to set
        """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError("user password must be string and not empty")

        self._password = value
        self._make_url()
        return

    def set_user_name(self, value: str):
        """
        Embed the user name in the handler

        :param value: the intended value to set
        """
        if not isinstance(value, str) or len(value) < 1:
            raise TypeError("user name must be string and not empty")

        self._user_name = value
        self._make_url()
        return

    def _make_url(self):

        self.url = "http://{0}".format(self._address)
        # self.url = "{0}:{1}@{2}".format(self.USER_NAME, self.PASSWORD, self.ADDRESS)

        if self._user_name is None or self._password is None:
            self._headers = None
        else:
            user_pass = self._user_name + ":" + self._password
            user_pass = base64.encodebytes(user_pass.encode("utf-8"))
            self._headers = {"Authorization": "Basic %s" % user_pass}
        return

    def _normalize_path(self, path, add_base=True):
        """

        :param path: the api element path, such as "status/gpio"
        :type path: str
        :param add_base: if T then start the path with /api/, else strip
        :type add_base: bool
        :return: the normalized path
        :rtype: str
        """
        if not isinstance(path, str):
            raise TypeError("path must be string")

        if self.trace is not None:
            # then assume is like logging
            self.trace.debug("path({0})".format(path))

        if path.startswith(self.API_BASE):
            # so starts with '/api'
            if not add_base:
                # then we do NOT want the '/api' preface
                path = path[5:]
            # else we do

        elif path.startswith(self.API_SEP):
            # so starts with '/status'
            path = path[1:]
            if add_base:
                # we already have the 'api/', so add leading SEP
                path = self.API_BASE + path

        elif path.startswith(self.API_RAW_BASE):
            if add_base:
                # we already have the 'api/', so add leading SEP
                path = self.API_SEP + path
            else:
                path = path[4:]

        elif add_base:
            # add the '/api'
            path = self.API_BASE + path

        return path
