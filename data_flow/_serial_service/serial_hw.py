__author__ = 'Lynn'

import serial

import serial_settings
from serial_object import SerialObject, SerialObjectException
from serial_publish import SerialStatsPublish


class SerialHardware(SerialObject):
    """
    A serial object which is 'real', so direct pyserial access
    """

    def __init__(self, my_instance_code):
        super().__init__(my_instance_code)
        self._type = self.TYPE_SERIAL

        # handle the control-signal/stats update to Router API
        base_path = "/status/{0}/stats/".format(self.get_name())
        self._stats = SerialStatsPublish(base_path, self._settings.api)

        # obtain the model type
        value = self.get_my_setting("product")
        self._stats.set_product_support_details(value)

        # limit how often we publish
        self._last_publish_time = 0
        self.publish_rate_seconds = 10

        self.serial = serial.Serial()
        # self.serial.name = self.get_my_setting("ser_port")
        self.serial.port = self.get_my_setting("ser_port")
        self.serial.baudrate = self.get_my_setting("baud")
        self.serial.parity = self.get_my_setting("parity")
        self.serial.bytesize = self.get_my_setting("databits")
        self.serial.stopbits = self.get_my_setting("stopbits")
        self.serial.timeout = 1.0

        # obtain if RTS/CTS flow control is True
        self.flow_control = self.get_my_setting("flow_control")
        self._stats.set_product_support_rtscts(self.flow_control == serial_settings.SER_FLOW_HW)
        self.serial.rtscts = False
        self.serial.xonxoff = False
        if self.flow_control == serial_settings.SER_FLOW_HW:
            self.serial.rtscts = True
        elif self.flow_control == serial_settings.SER_FLOW_SW:
            self.serial.xonxoff = True

        # read in the DTR/RTS output values
        self.dtr_out = self.get_my_setting("dtr_output")
        self.rts_out = self.get_my_setting("rts_output")
        return

    def open(self, params=None):
        """
        Open the port.

        :param params: optional parameters submitted as dictionary
        :type params: dict
        :return:

        """
        if params:  # for now, suppress warning
            pass
        self.serial.open()
        self.state = self.STATE_ACTIVE
        return True

    def write(self, data, now):
        """
        Send the data, which means for 'echo' we load into the recv buffer

        :param data:
        :param now:
        :return:
        """
        return self.serial.write(data)

    def read(self, now):
        """
        Receive any waiting data

        :param now:
        :return:
        """
        data = self.serial.read(1024)
        self.recv_buffer.process(data, now)
        return

    def tick(self, now: float):
        """
        Tick the buffer to handle timeouts, which for echo should do little
        :param now:
        :return:
        """
        if self.publish_rate_seconds > 0:
            if (now - self._last_publish_time) > self.publish_rate_seconds:
                if self._logger is not None:
                    self._logger.debug("Publish Now")
                self._last_publish_time = now
                self._publish_statistics(now)

        return self.recv_buffer.tick(now)

    def close(self):
        """
        Close the echo port

        :return:
        """
        self.state = self.STATE_DEFAULT
        self.recv_buffer.reset()
        return True

    def _publish_statistics(self, now: float, force=False):
        """
        Periodic refresh of the control signals (if available). This only handles change/RBX -
        any 'timing' period is handled by the caller

        :param now: the current time.time()
        :param force: if True, force the publish refresh
        :return:
        """
        change = False

        if self._stats.dtrdsr_out:
            # then have a DTR/DSR pair output - but we cannot read value
            if self.dtr_out == serial_settings.SER_DTR_ON:
                value = True
            elif self.dtr_out == serial_settings.SER_DTR_OFF:
                value = False
            else:
                assert self.dtr_out == serial_settings.SER_DTR_CONN
                # check on connection status?
                value = True
            self.serial.setDTR(value)
            change |= self._stats.publish_dtrdsr_output(value, force)

        if self._stats.dtrdsr_in:
            # then have a DTR/DSR pair input - read & refresh
            change |= self._stats.publish_dtrdsr_input(self.serial.getDSR(), force)

        if self.flow_control != serial_settings.SER_FLOW_HW:
            # we only update if NOT being used for HW flow control

            if self._stats.rtscts_out:
                # then have a RTS/CTS pair output - but we cannot read value
                if self.dtr_out == serial_settings.SER_DTR_ON:
                    value = True
                else:
                    assert self.dtr_out == serial_settings.SER_DTR_OFF
                    value = False
                self.serial.setRTS(value)
                change |= self._stats.publish_rtscts_output(value, force)

            if self._stats.rtscts_in:
                # then have a RTS/CTS pair input - read & refresh
                change |= self._stats.publish_rtscts_input(self.serial.getCTS(), force)

        if self._stats.cd_in:
            # then have a CD input - read & refresh
            change |= self._stats.publish_cd_input(self.serial.getCD(), force)

        if self._stats.ri_in:
            # then have a RI input - read & refresh
            change |= self._stats.publish_ri_input(self.serial.getRI(), force)

        # update the last activity time
        last = self.recv_buffer.last_data_time
        # TODO - compare to last send, update newest/max value
        change |= self._stats.publish_activity_time(last, force)

        return

# if __name__ == '__main__':
#
#     obj = SerialObject(2)
#
#     n = "Serial3"
#     x = obj.map_name_to_instance(n)
#     print("{0} = {1}".format(n, x))
