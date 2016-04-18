# Test the Data Core and objects

import unittest
import json

from data.data_types import data_type_python_to_internal, data_type_export_to_json, data_type_import_from_json, \
    validate_string, validate_name

import data.data_core as data_core
import data.data_object as data_object
from data.data_base import DataBase


class TestDataTypes(unittest.TestCase):

    def test_data_type_python_to_internal(self):

        self.assertEqual(data_type_python_to_internal(None), type(None))
        self.assertEqual(data_type_python_to_internal(1), float)
        self.assertEqual(data_type_python_to_internal(1.0), float)
        self.assertEqual(data_type_python_to_internal(""), str)
        self.assertEqual(data_type_python_to_internal("Object"), str)
        self.assertEqual(data_type_python_to_internal(True), bool)
        self.assertEqual(data_type_python_to_internal((0, 1)), list)
        self.assertEqual(data_type_python_to_internal([0, 1]), list)
        with self.assertRaises(TypeError):
            data_type_python_to_internal({0: True})

        self.assertEqual(data_type_python_to_internal(int), float)
        self.assertEqual(data_type_python_to_internal(float), float)
        self.assertEqual(data_type_python_to_internal(str), str)
        self.assertEqual(data_type_python_to_internal(bool), bool)
        self.assertEqual(data_type_python_to_internal(tuple), list)
        self.assertEqual(data_type_python_to_internal(list), list)
        self.assertEqual(data_type_python_to_internal(type(None)), type(None))
        with self.assertRaises(TypeError):
            data_type_python_to_internal(dict)

    def test_data_type_export_to_json(self):

        self.assertEqual(data_type_export_to_json(None), 'null')
        self.assertEqual(data_type_export_to_json(1), 'num')
        self.assertEqual(data_type_export_to_json(1.0), 'num')
        self.assertEqual(data_type_export_to_json(""), 'str')
        self.assertEqual(data_type_export_to_json("Object"), 'str')
        self.assertEqual(data_type_export_to_json(True), 'bool')
        # ((0, 1), 'list'),
        # ([0, 1], 'list'),
        with self.assertRaises(TypeError):
            data_type_python_to_internal({0: True})

        self.assertEqual(data_type_export_to_json(int), 'num')
        self.assertEqual(data_type_export_to_json(float), 'num')
        self.assertEqual(data_type_export_to_json(str), 'str')
        self.assertEqual(data_type_export_to_json(bool), 'bool')
        self.assertEqual(data_type_export_to_json(tuple), 'list')
        self.assertEqual(data_type_export_to_json(list), 'list')
        self.assertEqual(data_type_export_to_json(type(None)), 'null')
        with self.assertRaises(TypeError):
            data_type_python_to_internal(dict)

    def test_data_type_import_from_json(self):

        self.assertEqual(data_type_import_from_json('null'), type(None))
        self.assertEqual(data_type_import_from_json('num'), float)
        self.assertEqual(data_type_import_from_json('str'), str)
        self.assertEqual(data_type_import_from_json('bool'), bool)
        self.assertEqual(data_type_import_from_json('list'), list)
        self.assertEqual(data_type_import_from_json('NULL'), type(None))
        self.assertEqual(data_type_import_from_json('Num'), float)
        self.assertEqual(data_type_import_from_json('Str'), str)
        self.assertEqual(data_type_import_from_json('bOol'), bool)
        self.assertEqual(data_type_import_from_json('lisT'), list)
        with self.assertRaises(TypeError):
            data_type_import_from_json(None)
            data_type_import_from_json(float)
            data_type_import_from_json('happy')

    def test_validate_string(self):

        self.assertEqual(validate_string(None), '')
        self.assertEqual(validate_string(""), '')
        self.assertEqual(validate_string("Object"), 'Object')
        self.assertEqual(validate_string("Tommy!"), 'Tommy!')
        self.assertEqual(validate_string("Hello\u0024"), 'Hello$')

        with self.assertRaises(TypeError):
            validate_string(1)

        with self.assertRaises(ValueError):
            validate_string("\x00")
            validate_string("Hello\n")
            validate_string("\x80abc")
            validate_string("Hello\"")

    def test_validate_name(self):

        self.assertEqual(validate_name("hello"), "hello")
        self.assertEqual(validate_name("Hello"), "hello")
        self.assertEqual(validate_name("HELLO"), "hello")
        self.assertEqual(validate_name("7hello"), "7hello")
        self.assertEqual(validate_name("HELLO_WORLD"), "hello_world")
        self.assertEqual(validate_name("HELLO-WORLD"), "hello-world")

        with self.assertRaises(TypeError):
            validate_name(1)

        with self.assertRaises(ValueError):
            validate_name(None)
            validate_name("")
            validate_name("HELLO WORLD")
            validate_name("HELLO.WORLD")
            validate_name("HELLO/WORLD")
            validate_name("HELLO\\WORLD")
            validate_name("Tommy!")

    def test_data_core_description(self):

        root = data_core.DataCore('root')
        assert isinstance(root, data_object.DataObject)

        self.assertEqual(root.set_description(None), None)
        self.assertEqual(root.get_description(), None)
        self.assertEqual(root.set_description(""), None)
        self.assertEqual(root.get_description(), None)
        self.assertEqual(root.set_description("Hello to you all"), "Hello to you all")
        self.assertEqual(root.get_description(), "Hello to you all")

        with self.assertRaises(TypeError):
            root.set_description(1)

        with self.assertRaises(ValueError):
            root.set_description("Hello to you all\n")
            root.set_description("Hello to \" you all")

        # clear out the description, after it has been set
        self.assertEqual(root.set_description(None), None)
        self.assertEqual(root.get_description(), None)

    def test_data_core_user_tag(self):

        root = data_core.DataCore('root')

        self.assertEqual(root.set_user_tag(None), None)
        self.assertEqual(root.get_user_tag(), None)
        self.assertEqual(root.set_user_tag(""), None)
        self.assertEqual(root.get_user_tag(), None)
        self.assertEqual(root.set_user_tag("AST#023674-A"), "AST#023674-A")
        self.assertEqual(root.get_user_tag(), "AST#023674-A")

        with self.assertRaises(TypeError):
            root.set_user_tag(1)

        with self.assertRaises(ValueError):
            root.set_user_tag("AST#023674-A\n")
            root.set_user_tag("AST#023674\"A")

        # clear out the user asset tag, after it has been set
        self.assertEqual(root.set_user_tag(None), None)
        self.assertEqual(root.get_user_tag(), None)

    def test_data_core_export_json(self):

        root = data_core.DataCore('root')

        expect = '{"class": "DataCore", "name": "root"}'
        self.assertEqual(root.export_json(), expect)

    def test_data_object_data_typing(self):

        root = data_object.DataObject('root')

        self.assertEqual(root.validate_data_type(None), type(None))
        # self.assertEqual(root.get_json_data_type(None), 'null')

        self.assertEqual(root.validate_data_type(1), float)
        self.assertEqual(root.get_json_data_type(1), 'num')
        self.assertEqual(root.validate_data_type(1.0), float)
        self.assertEqual(root.get_json_data_type(1.0), 'num')
        self.assertEqual(root.validate_data_type("hello"), str)
        self.assertEqual(root.get_json_data_type("hello"), 'str')
        self.assertEqual(root.validate_data_type(True), bool)
        self.assertEqual(root.get_json_data_type(True), 'bool')

    def test_data_object_export_json(self):

        root = data_object.DataObject('root')

        expect = '{"class": "DataObject", "name": "root", "data_type": "num"}'
        self.assertEqual(root.export_json(), expect)

    def test_data_object_list(self):

        model = {"class": "DataObject", "name": "min", "data_type": "num", "value": 10, "uom": "gal"}
        source = json.dumps(model)

        root = data_object.DataObject('root')
        root.set_as_root()
        root.import_json(source)
        # report = root.my_report()
        # for line in report:
        #     print('report:%s' % line)

        result = root.export_json()
        self.assertEqual(type(result), str)
        result = json.loads(result)
        self.assertEqual(result["class"], model["class"])
        self.assertEqual(result["value"], model["value"])
        self.assertEqual(result["uom"], model["uom"])
        self.assertEqual(result["data_type"], model["data_type"])

        model = {"class": "DataObject", "name": "stats", "child": [
            {"class": "DataObject", "name": "min", "data_type": "num", "value": 10, "uom": "gal"},
            {"class": "DataObject", "name": "max", "data_type": "num", "value": 34, "uom": "gal"},
            {"class": "DataObject", "name": "avg", "data_type": "num", "value": 28, "uom": "gal"},
            {"class": "DataObject", "name": "period", "data_type": "num", "value": 1, "uom": "day"}
        ]}
        source = json.dumps(model)

        root = data_object.DataObject('root')
        root.set_as_root()
        root.import_json(source)

        # report = root.my_report()
        # for line in report:
        #     print('report:%s' % line)

        result = root.export_json()
        result = json.loads(result)
        # print('result[{0}]:{1}'.format(len(result), result))
        expect = '{"class": "DataObject", "name": "stats", "data_type": "num", "child": [' + \
                 '{"class": "DataObject", "name": "min", "value": 10, "data_type": "num", "uom": "gal"}, ' + \
                 '{"class": "DataObject", "name": "max", "value": 34, "data_type": "num", "uom": "gal"}, ' + \
                 '{"class": "DataObject", "name": "avg", "value": 28, "data_type": "num", "uom": "gal"}, ' + \
                 '{"class": "DataObject", "name": "period", "value": 1, "data_type": "num", "uom": "day"}' + \
                 ']}'
        expect = json.loads(expect)
        self.assertEqual(result, expect)

        model = {"class": "DataObject", "data_type": "list", "name": "tank_a", "child": [
            {"class": "DataSetting", "data_type": "str", "name": "update_rate", "value": "10 min"},
            {"class": "DataObject", "data_type": "num", "name": "level", "value": 10, "uom": "gal"},
            {"class": "DataObject", "data_type": "str", "name": "contents", "value": "Unleaded"},
            {"class": "DataObject", "data_type": "list", "name": "stats", "child": [
                {"class": "DataObject", "data_type": "num", "name": "min", "value": 10, "uom": "gal"},
                {"class": "DataObject", "data_type": "num", "name": "max", "value": 34, "uom": "gal"},
                {"class": "DataObject", "data_type": "num", "name": "avg", "value": 28, "uom": "gal"},
                {"class": "DataObject", "data_type": "num", "name": "period", "value": 1, "uom": "day"}
            ]}
        ]}
        source = json.dumps(model)

        root = data_core.DataCore('root')
        root.set_as_root()
        root.import_json(source)
        # report = root.my_report()
        # for line in report:
        #     print('report:%s' % line)

        result = root.export_json()
        result = json.loads(result)
        # print('result[{0}]:{1}'.format(len(result), result))
        expect = '{"child": [{"data_type": "str", "value": "10 min", "class": "DataSetting", "name": "update_' + \
                 'rate"}, {"data_type": "num", "value": 10, "uom": "gal", "class": "DataObject", "name": "' + \
                 'level"}, {"data_type": "str", "value": "Unleaded", "class": "DataObject", "name": "contents"}, ' + \
                 '{"data_type": "list", "child": [{"data_type": "num", "value": 10, "uom": "gal", "class": ' + \
                 '"DataObject", "name": "min"}, {"data_type": "num", "value": 34, "uom": "gal", "class": ' + \
                 '"DataObject", "name": "max"}, {"data_type": "num", "value": 28, "uom": "gal", "class": ' + \
                 '"DataObject", "name": "avg"}, {"data_type": "num", "value": 1, "uom": "day", "class": ' + \
                 '"DataObject", "name": "period"}], "class": "DataObject", "name": "stats"}], "class": ' + \
                 '"DataObject", "name": "tank_a"}'
        expect = json.loads(expect)
        self.assertEqual(result, expect)

    def test_build_model(self):

        root = data_object.DataObject('root')
        base = root.get_core_data_base()
        assert isinstance(base, DataBase)
        base.set_root(root)

        source = make_it()
        root.import_json(source)
        report = root.my_report()
        for line in report:
            print('report:%s' % line)

        result = root.export_json()
        print('export JSON:%s' % result)

        print("Object names:{0}".format(base.build_object_names()))

        print("Root name:{0}".format(base.get_root().get_name()))

        print("== Show indexed list")
        index = 0
        value = base.get_array_list()
        for item in value:
            print("%02d %s" % (index, item.get_full_name()))
            index += 1

        # logger.debug("== Show keyed list of objects")
        # value_list = base.get_dict_of_data_object()
        # for key, value in value_list.iteritems():
        #     logger.debug("%02d %s", value.get_index(), key)

        # logger.debug("== Show keyed list of list")
        # value_list = base.get_dict_of_data_list()
        # for key, value in value_list.iteritems():
        #     logger.debug("%02d %s", value.get_index(), key)

        return


def make_it():
    """

    :rtype: str
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
    source = json.dumps(model)
    return source

if __name__ == '__main__':
    unittest.main()
