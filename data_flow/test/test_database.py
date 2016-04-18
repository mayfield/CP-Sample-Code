# Test the Data Base concept

import unittest
import json
import logging

import data.data_object as data_object
from data.data_template import BoolTemplate
import data.data_base as data_base


class TestDataBase(unittest.TestCase):

    def test_model_rs232(self):

        data_base._core_database = None

        # Start by creating a DateBase
        base = data_base.DataBase('_world')
        self.assertTrue(isinstance(base, data_base.DataBase))
        base.logger.setLevel(logging.INFO)

        # add a template for the RS232 control signals
        template_name = 'control_lines'
        template = BoolTemplate(template_name)
        base.add_to_data_base(template)
        template_full_name = template.get_full_name()

        self.assertTrue(template.set_attribute('display_name_true', "active"))
        self.assertTrue(template.set_attribute('display_name_false', "idle"))
        self.assertTrue(template.set_attribute('display_color_true', ("forestgreen", "ghostwhite")))
        self.assertTrue(template.set_attribute('display_color_false', ("gray", "black")))
        self.assertTrue(template.set_attribute('abnormal_when', False))

        # add the first RS232 object
        port_name = 'serial_1'
        port_object = data_object.DataObject(port_name)

        # arrange the parent, which is the raw data root
        # port_object.set_parent(base.get_data_root())
        base.add_to_data_base(port_object)

        self.assertEqual(port_object.get_attribute('data_name'), port_name)
        self.assertEqual(port_object.get_attribute('class'), 'DataObject')
        # 'display_name' is special, will return 'data_name'
        self.assertEqual(port_object.get_attribute('display_name'), port_name)

        self.assertFalse(port_object.set_attribute('silly_shoes', 10))

        self.assertTrue(port_object.set_attribute('description', "First serial port"))
        self.assertTrue(port_object.set_attribute('data_type', "base"))

        #
        # add the first RS232 object - DTR OUTPUT
        control_name = 'dtr_out'
        control_object = data_object.BooleanObject(control_name)

        port_object.add_child(control_object)
        control_object.set_template(template)
        base.add_to_data_base(control_object)
        self.assertEqual(control_object.get_attribute('data_name'), control_name)
        self.assertEqual(control_object.get_attribute('class'), 'BooleanObject')

        self.assertTrue(control_object.set_attribute('description', "DTR/DSR pair output"))
        self.assertTrue(control_object.set_attribute('data_type', "digital"))
        self.assertTrue(control_object.set_attribute('read_only', False))

        # confirm inherited from template
        self.assertEqual(template.get_attribute('display_name_true'), "active")
        self.assertEqual(template.get_attribute('display_name_false'), "idle")

        # add the second RS232 object - DSR input
        control_name = 'dsr_in'
        control_object = data_object.BooleanObject(control_name)

        port_object.add_child(control_object)
        control_object.set_template(template)
        base.add_to_data_base(control_object)
        self.assertEqual(control_object.get_attribute('data_name'), control_name)
        self.assertEqual(control_object.get_attribute('class'), 'BooleanObject')

        self.assertTrue(control_object.set_attribute('description', "DTR/DSR pair input"))
        self.assertTrue(control_object.set_attribute('data_type', "digital"))
        self.assertTrue(control_object.set_attribute('read_only', True))

        # print("attrib:{0}".format(control_object._attrib))

        # data_base.print_base_report(base)

        result = base.find_data_object(template_full_name)
        assert result is None
        result = base.find_setting_object(template_full_name)
        assert result is None
        result = base.find_template_object(template_full_name)
        assert result == template

        data_base._core_database = None

        return

    def test_split_path(self):

        data_base._core_database = None

        base = data_base.get_core_database()
        self.assertTrue(isinstance(base, data_base.DataBase))

        path = "data/tank/alarm"
        # print("Result:{0}".format(base.split_object_path(path)))
        self.assertEqual(base.split_object_path(path), ["data", "tank", "alarm"])
        path = "/data/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["data", "tank", "alarm"])
        path = "/data/tank/alarm/"
        self.assertEqual(base.split_object_path(path), ["data", "tank", "alarm"])

        path = "c:/users/linse/data/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["data", "tank", "alarm"])
        path = "c:/users/linse/data/tank/alarm/"
        self.assertEqual(base.split_object_path(path), ["data", "tank", "alarm"])

        path = "c:/users/linse/templates/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["templates", "tank", "alarm"])
        path = "c:/users/linse/settings/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["settings", "tank", "alarm"])
        path = "c:/users/linse/status/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["status", "tank", "alarm"])
        path = "c:/users/linse/config/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["config", "tank", "alarm"])
        path = "c:/users/linse/state/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["state", "tank", "alarm"])
        path = "c:/users/linse/control/tank/alarm"
        self.assertEqual(base.split_object_path(path), ["control", "tank", "alarm"])

        # ('data', 'templates', 'settings', 'status', 'config', 'state', 'control')

        # these are not valid 'path', so ValueError thrown
        path = ""
        with self.assertRaises(ValueError):
            base.split_object_path(path)
        path = None
        with self.assertRaises(ValueError):
            base.split_object_path(path)
        path = 23
        with self.assertRaises(ValueError):
            base.split_object_path(path)

        # these are too short, or lack the correct API name (like 'data' or 'config')
        path = "c:/users/linse/tank/alarm"
        self.assertEqual(base.split_object_path(path), [])
        path = "alarm"
        self.assertEqual(base.split_object_path(path), [])

        data_base._core_database = None

        return

    def test_fetch_path_objects(self):

        data_base._core_database = None
        base = data_base.get_core_database()
        self.assertTrue(isinstance(base, data_base.DataBase))

        path = "data/tank/alarm"
        result = base.fetch_object_path_list(path)
        # print("Result:{0}".format(result))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_name(), 'data')

        path = "templates/tank/alarm"
        result = base.fetch_object_path_list(path)
        # print("Result:{0}".format(result))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_name(), 'templates')

        path = "settings/tank/alarm"
        result = base.fetch_object_path_list(path)
        # print("Result:{0}".format(result))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_name(), 'settings')

        path = "config/tank/alarm"
        with self.assertRaises(ValueError):
            base.fetch_object_path_list(path)

        data_base._core_database = None

        return


def make_it(as_json=True):
    """

    :rtype: str or dict
    """
    model = {"class": "DataObject", "name": "root", "child": [
        {"class": "DataObject", "name": "system", "child": [
            {"class": "DataObject", "name": "version", "data_type": "num", "value": 2.72},
            {"class": "DataObject", "name": "build", "data_type": "str", "value": "2015-Mar-06"}
        ]},
        {"class": "DataObject", "name": "templates", "child": [
            {"class": "DataTemplate", "name": "period", "data_type": "num", "uom": "sec",
             "description": "Time period such as '10 min' or '600'"},
            {"class": "DataTemplate", "name": "tank_level", "data_type": "num", "uom": "gal",
             "min_value": 0, "max_value": 50000, "description": "Tank Level between 0 to 50000"},
        ]},
        {"class": "DataObject", "name": "tank_a", "child": [
            {"class": "DataSetting", "name": "update_rate", "data_type": "str", "value": "10 min"},
            {"class": "DataObject", "name": "level", "template": "tank_level", "value": 10},
            {"class": "DataObject", "name": "contents", "data_type": "str", "value": "Unleaded"},
            {"class": "DataObject", "name": "stats", "child": [
                {"class": "DataObject", "name": "min", "template": "tank_level", "value": 10},
                {"class": "DataObject", "name": "max", "template": "tank_level", "value": 34},
                {"class": "DataObject", "name": "avg", "template": "tank_level", "value": 28},
                {"class": "DataObject", "name": "period", "data_type": "num", "value": 1, "uom": "day"}
            ]}
        ]},
        {"class": "DataObject", "name": "tank_b", "child": [
            {"class": "DataObject", "name": "level", "template": "num", "value": 75},
            {"class": "DataObject", "name": "contents", "data_type": "str", "value": "Premium"},
            {"class": "DataObject", "name": "stats", "child": [
                {"class": "DataObject", "name": "min", "template": "tank_level", "value": 10},
                {"class": "DataObject", "name": "max", "template": "tank_level", "value": 34},
                {"class": "DataObject", "name": "avg", "template": "tank_level", "value": 28},
                {"class": "DataObject", "name": "period", "data_type": "num", "value": 1, "uom": "day"}
            ]}
        ]},
    ]}
    if as_json:
        # convert dict to string
        model = json.dumps(model)

    return model


if __name__ == '__main__':

    unittest.main()
