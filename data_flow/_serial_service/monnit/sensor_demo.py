
import logging
import time


class SensorDemo(object):

    # used for sliding averages. Set to 1 to disable,
    AVG_BATTERY = 0.25
    AVG_RSSI = 0.9

    def __init__(self, device_id=0):
        """

        :param device_id: the sensor device id
        :return:
        """
        self._attrib = {'dev_id': device_id, 'sensor_value1': None}
        self.device_id = device_id
        self._last_data = None

        self.alerts = {
            95411: {'desc': "Alert: Humidity"},
            95412: {'desc': "Alert: Manager's Door After Hours",
                    'tag': ("Door Open", "Door Closed"), 'email': 'all'},
            95413: {'desc': "Alert: S8892 W broadway Power Status",
                    'tag': ("Lost Power", "Power Okay"), 'email': 'all'},
            96001: {'desc': "Alert: PIR"},
            96002: {'desc': "Alert: Temperature"},
        }
        return

    def process_data(self, response):
        """

        Response should be a parsed dictionary of this sort:
        {'code': 86, 'time_str': '2010-01-01 07:00:00 UTC', 'time': 1262329200.0, 'battery': 2.99,
         'sensor_type': 9, 'dev_rssi': -38, 'sensor_value1': False, 'ap_rssi': -38,
         'sensor_uom1': 'open', 'dev_id': 95412, 'sensor_state': 2}

        :param response:
        :type response: dict
        :return:
        """
        from monnit.email_client import send_email

        assert isinstance(response, dict)
        if response['code'] != 0x56:
            logging.error("data:{}".format(response))
            raise ValueError("Sensor.process() only allows data_log/0x56 messages")

        self._last_data = response

        first_data = False
        if 'sensor_type' not in self._attrib:
            # then is first message!
            logging.info("First data seen for device id:%d" % self.device_id)
            self._attrib['sensor_type'] = self._last_data['sensor_type']
            first_data = True

        elif self._attrib['sensor_type'] != self._last_data['sensor_type']:
            logging.error("data:{}".format(response))
            raise ValueError("Sensor.process() new data wrong type")

        # check the time
        if self._last_data['time'] != 0.0:
            # then save this time
            self._attrib['time'] = self._last_data['time']
        else:  # use server time
            self._attrib['time'] = time.time()

        # import the basic stats - RSSI etc
        self._do_one_import_averaging('battery', self.AVG_BATTERY)
        self._do_one_import_averaging('dev_rssi', self.AVG_RSSI)
        self._do_one_import_averaging('ap_rssi', self.AVG_RSSI)

        self._do_one_min_max('battery', 'bat_min', 'bat_max')
        self._do_one_min_max('dev_rssi', 'dev_rssi_min', 'dev_rssi_max')
        self._do_one_min_max('ap_rssi', 'ap_rssi_min', 'ap_rssi_max')

        value = self._last_data['sensor_value1']
        if self._attrib['sensor_value1'] == value:
            pass
            # logging.debug("[sensor_value1] did not change")
        else:
            self._attrib['sensor_value1'] = value
            self._attrib['sensor_uom1'] = self._last_data['sensor_uom1']
            # logging.debug("[sensor_value1] == {}".format(self._attrib['sensor_value1']))

            my_alert = self.alerts[self.device_id]
            message = " %s = " % my_alert['desc']

            if 'tag' in my_alert:
                # then is digital value, so 'tag' = (when_false, when_true)
                if value:  # when True, use second tag
                    message += my_alert['tag'][1]
                else:  # when false, use first tag
                    message += my_alert['tag'][0]

            if 'time' in self._last_data:
                now = self._last_data['time']
            else:  # use NOW
                now = time.time()

            message_full = message + time.strftime(" (%Y-%m-%d %H:%M:%S %Z)", time.localtime(now))

            logging.info(message_full)

            if 'email' in my_alert and not first_data:
                # we skip the update if the first data
                email_mode = my_alert['email']
                if email_mode is not None:
                    start = time.time()
                    send_email(subject=message, body=message_full)
                    end = time.time()
                    logging.debug("Email Sent: %d seconds" % (end - start))
                    time.sleep(2.0)

        return

    def report(self):
        """
        Create a string report

        :return:
        """
        report = "Sensor:%d" % self.device_id
        if self._last_data is None:
            report += " is offline/undetected."
        else:
            report += " %s %s\t" % (self._attrib['sensor_value1'], self._attrib['sensor_uom1'])
            report += time.strftime("%H:%M:%S", time.localtime(self._attrib['time']))
            report += " bat:%0.2fv" % self._attrib['battery']
            report += " AP:%d (%d:%d)" % (self._attrib['ap_rssi'], self._attrib['ap_rssi_min'],
                                          self._attrib['ap_rssi_max'])
            report += " DV:%d (%d:%d)" % (self._attrib['dev_rssi'], self._attrib['dev_rssi_min'],
                                          self._attrib['dev_rssi_max'])
        return report

    def _do_one_import_averaging(self, tag, avg_new):
        """

        :param tag: the keyed data name
        :type tag: str
        :param avg_new: the % as 0.0 to 1.0, such as 0.25, means 75% is old and 25% is new
        :type avg_new: float
        :return:
        """
        assert 0.0 < avg_new <= 1.0
        if tag in self._last_data:
            # only do this if that tag in the parsed data
            value = self._last_data[tag]

            if tag not in self._attrib or avg_new == 1.0:
                # the first setting, or not doing averaging
                self._attrib[tag] = value
                # logging.debug("{0}[{1}] forced to {2}".format(self.device_id, tag, value))

            elif self._attrib[tag] != value:
                # only bother with the computation if it changes anything
                old = self._attrib[tag]
                self._attrib[tag] = round((old * (1.0 - avg_new)) + (value * avg_new), 2)
                # logging.debug("{0}.[{1}] new:{2} ({3} to {4})".format(
                #         self.device_id, tag, value, old, self._attrib[tag]))

            # ELSE, we are doing averaging, but the value did not change

        return

    def _do_one_min_max(self, tag, tag_min, tag_max):
        """

        :param tag: the keyed data name
        :type tag: str
        :param tag_min: the keyed data name
        :type tag_min: str
        :param tag_max: the keyed data name
        :type tag_max: str
        :return:
        """
        value = self._last_data[tag]
        if tag_min not in self._attrib or value < self._attrib[tag_min]:
            self._attrib[tag_min] = value
        if tag_max not in self._attrib or value > self._attrib[tag_max]:
            self._attrib[tag_max] = value
        return
