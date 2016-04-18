__author__ = 'Lynn'

from serial_settings import SerialSettings
from serial_buffer import SerialBuffer


# use when a serial object is in a bad state, etc
class SerialObjectException(Exception):
    pass


# use when a serial object is asked to do something it doesn't have!
class SerialNoSupport(Exception):
    pass


class SerialObject(object):
    """
    The serial object represents the actual serial "port" or device - one exists for every serial
    target.
    """

    # we use this, like 'serial_3'
    NAME_BASE = 'serial'

    # allow setting to 0 or 1, so "COM1" is either 'serial_0' or 'serial_1'
    NAME_OFFSET = 1

    STATE_FREE = 'closed'
    STATE_IDLE = 'idle'
    STATE_ACTIVE = 'active'
    STATE_DEFAULT = STATE_FREE

    TYPE_ECHO = 'echo'
    TYPE_SERIAL = 'serial'
    TYPE_USB = 'usb'
    TYPE_IP_BASIC = 'ip_basic'
    TYPE_IP_FULL = 'ip_full'

    def __init__(self, my_instance_code):
        self._settings = SerialSettings()
        self._max_port = self.get_global_setting("max_ports")

        # my_instance is zero-based
        assert 0 <= my_instance_code < self._max_port
        self.my_code = my_instance_code
        # my_name shall be like "serial_1" for instance 0
        self.my_name = "{0}_{1}".format(self.NAME_BASE, str(self.my_code + self.NAME_OFFSET))
        self.state = self.STATE_DEFAULT
        self._type = self.TYPE_ECHO

        self.recv_buffer = SerialBuffer()

        self._parent = None
        self._logger = None

        return

    def __repr__(self):
        return self.get_name()

    def get_name(self):
        """
        Get the internal name, which shall be like 'serial_1' for instance 0
        :return:
        """
        return self.my_name

    def set_parent(self, parent):
        self._parent = parent
        return

    def set_logger(self, logger):
        self._logger = logger

    def get_buffer_size(self):
        return len(self.recv_buffer)

    def get_global_setting(self, name):
        return self._settings.get_value(name, None)

    def get_my_setting(self, name):
        return self._settings.get_value(name, self.my_code)

    def set_echo_mode(self):
        """
        Bundle the settings for 'echo' mode.

        :return:
        """
        self.state = self.STATE_DEFAULT
        self._type = self.TYPE_ECHO

        # set high timeouts, as we want the buffer to accumulate data until asked for
        self.recv_buffer.reset()
        self.recv_buffer.recv_idle_pack_seconds = 3600
        self.recv_buffer.recv_idle_discard_seconds = 3600 + 60

        return

    def map_instance_to_name(self, instance_number):
        """
        Given a name like COM1 or /dev/ttyS0 or /dev/ttyUSB2. Although pySerial (& other mods) might handle
        we want one which can handle special cases for Routers

        :param instance_number:
        :type instance_number: int
        :return:
        """
        if not isinstance(instance_number, int):
            raise TypeError("Serial Port instance must be type=int")

        if not (0 <= instance_number < self._max_port):
            if self._max_port == 1:
                raise ValueError("Serial Port instance must be 0/zero")
            else:
                raise ValueError("Serial Port instance must be between 0/zero and {0}".format(self._max_port - 1))

        return self.NAME_BASE + str(instance_number)

    @staticmethod
    def map_name_to_instance(name):
        """
        Given a name like COM1 or /dev/ttyS0 or /dev/ttyUSB2. Although pySerial (& other mods) might handle
        we want one which can handle special cases for Routers

        :param name:
        :type name: str
        :return:
        """
        if not isinstance(name, str):
            raise TypeError("Serial Port name must be type=str")

        x = name.lower()

        if x.startswith('serial'):
            # then our internal method, such as serial1 = 0, etc.
            value = int(x[6:]) - 1

        elif x.startswith('com'):
            # then the Windows style, call COM1 = 0, etc.
            value = int(x[3:]) - 1

        elif x.startswith('/dev/ttys'):
            # then the Linux style, call /dev/ttys0 = 0, etc.
            value = int(x[9:])

        elif x.startswith('/dev/ttyusb'):
            # then the Linux style, call /dev/ttys0 = 0, etc.
            value = int(x[11:])

        else:
            raise ValueError("Unknown serial port name:{}".format(name))

        return value

    def get_report(self):
        """
        :return:
        """
        result = dict()
        result['name'] = self.get_name()
        result['status'] = self.state
        return result

    def open(self, params=None):
        """
        Open the port. In base class this is a null/echo port.

        :param params: optional parameters submitted as dictionary
        :type params: dict
        :return:

        """
        if params:  # for now, suppress warning
            pass
        self.set_echo_mode()
        self.state = self.STATE_ACTIVE
        return True

    def write(self, data, now):
        """
        Send the data, which means for 'echo' we load into the recv buffer

        :param data:
        :param now:
        :return:
        """
        if self.state != self.STATE_ACTIVE:
            raise SerialObjectException("Port {0} not open".format(self.get_name()))

        self.recv_buffer.process(data, now)
        return len(data)

    def read(self, now):
        """
        Receive any waiting data

        :param now:
        :return:
        """
        if self.state != self.STATE_ACTIVE:
            if now:  # suppress unused warning
                pass
            raise SerialObjectException("Port {0} not open".format(self.get_name()))

        return self.recv_buffer.data_get()

    def tick(self, now):
        """
        Tick the buffer to handle timeouts, which for echo should do little
        :param now:
        :return:
        """
        return self.recv_buffer.tick(now)

    def close(self):
        """
        Close the echo port

        :return:
        """
        self.state = self.STATE_DEFAULT
        self.recv_buffer.reset()
        return True

# if __name__ == '__main__':
#
#     obj = SerialObject(2)
#
#     n = "Serial3"
#     x = obj.map_name_to_instance(n)
#     print("{0} = {1}".format(n, x))
