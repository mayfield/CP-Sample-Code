# Test the Monnit Sensor Data code

import unittest
import logging

import monnit.sensor_data as sensor_data


class TestAny(unittest.TestCase):

    def test_update_network_state_req(self):

        obj = sensor_data.MonnitSensorData()

        # test Sensor type 02 (temperature)
        raw = b'\x02\x00\x22\xf2\xd8'
        result = obj.parse_any({}, raw)
        logging.debug("Test {0}".format(result))
        self.assertEqual(result['sensor_type'], 2)

        # test Sensor type 03 (dry contact)
        raw = b'\x03\x00\x00\x01\x00'
        result = obj.parse_any({}, raw)
        # logging.debug("Test {0}".format(result))
        self.assertEqual(result['sensor_type'], 3)
        self.assertEqual(result['sensor_value1'], True)
        raw = b'\x03\x00\x00\x00\x00'
        result = obj.parse_any({}, raw)
        self.assertEqual(result['sensor_type'], 3)
        self.assertEqual(result['sensor_value1'], False)

        # test Sensor type 09 (open close)
        raw = b'\x09\x00\x00\x01\x00'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 9)
        self.assertEqual(result['sensor_value1'], True)
        raw = b'\x09\x00\x00\x00\x00'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 9)
        self.assertEqual(result['sensor_value1'], False)

        # test Sensor type 23 (PIR Motion)
        raw = b'\x17\x00\x00\x01'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 23)
        self.assertEqual(result['sensor_value1'], True)
        raw = b'\x17\x00\x00\x00'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 23)
        self.assertEqual(result['sensor_value1'], False)

        # test Sensor type 43 (humidity)
        raw = b'\x2B\x00\x00\x72\x09\x61\x09'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 43)
        self.assertEqual(result['sensor_value1'], 24.01)
        self.assertEqual(result['sensor_value2'], 75.52)
        raw = b'\x2B\x00\x00\x53\x09\x3e\x09'
        result = obj.parse_any({}, raw)
        logging.debug("Result:" + obj.show_any(result))
        self.assertEqual(result['sensor_type'], 43)
        self.assertEqual(result['sensor_value1'], 23.66)
        self.assertEqual(result['sensor_value2'], 74.97)

        return


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
