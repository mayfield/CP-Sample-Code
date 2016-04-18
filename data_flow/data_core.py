# File: data_core.py
# Desc: the base class for the morsel project

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#

"""\
The data objects:

Attributes:
[
        self._required_keys = ['class', 'data_name', 'data_type']

Optional Attribute:
['description'] The user description, which is unicode. The description is usually something like
        "outdoor ambient temperature", or "the door switch on north wall".

['user_tag'] The user asset tag, which is unicode. The user asset tag is a user-assigned tag, such
        as "NE16273", which is used to identify something in other systems. It likely must be unique,
        however no uniqueness is enforced here!

"""

import copy
import json

from data.data_types import validate_name, data_type_import_from_json

__version__ = "1.0.0"


class DataCore(object):

    PATH_SEP = '.'

    # valid ['class'] values
    CLASS_ALL = ('DataCore', 'DataObject', 'DataSetting', 'DataAlarm', 'DataTemplate')

    # a shared/singlton reference to the database
    _CORE_DATABASE = None

    API_PATH_TEMPLATE = 'config/template'

    def __init__(self, name):

        self._attrib = dict()
        self._attrib['data_name'] = name
        self._attrib['class'] = 'DataCore'
        self._attrib['index'] = -1
        self._attrib['path'] = None
        self._attrib['role'] = "core"
        self._trace = None

        self._required_keys = ['class', 'data_name']
        # these are always special ['data_type']

        # we only have a single parent in the name hierarchy
        self._parent = None

        # these are the sub-values - _children_keyed only set when _children_list > len 0
        self._children_list = list()
        self._children_keyed = None

        # a 'template' is kind of a stand-in for us, processing input in a consistent SHARED
        # manner, such as 10 tanks all having same POLL RATE or Min/Max fill levels.
        self._template = None

        # a special value, used to define object for use INTERNALLY
        self._private = False

        return

    @staticmethod
    def code_name():
        return 'DataCore'

    @staticmethod
    def code_version():
        return __version__

    def __getitem__(self, key):
        return self._attrib[key]

    def __setitem__(self, key, value):
        self._attrib[key] = value

    def __str__(self):
        return '%s(%s)' % (self.code_name(), self['data_name'])

    def __len__(self):
        return len(self._children_list)

    def get_core_data_base(self):
        """
        Any object can give us a 'database' reference
        :return:
        :rtype: DataBase
        """
        if self._CORE_DATABASE is None:
            # then init our singleton
            from data.data_base import DataBase

            DataCore._CORE_DATABASE = DataBase('core')

        return self._CORE_DATABASE

    def get_name(self):
        return self['data_name']

    def get_full_name(self):
        """
        Obtain my full name. which is my name appended to my parent's name
        :return:
        """
        if 'path' not in self._attrib or self['path'] is None:
            self.refresh_full_name()
        return self['path']

    def refresh_full_name(self):
        """
        Obtain my full name. which is my name appended to my parent's name
        :return:
        """
        if self._parent is None:
            # then I am the root database, so return nothing (just the separator)
            self['path'] = self.PATH_SEP

        else:
            value = self._parent.get_full_name()
            if value == self.PATH_SEP:
                # then first level, but we don't want 2 dots
                self['path'] = self.PATH_SEP + self.get_name()

            else:  # else is sub level
                self['path'] = value + self.PATH_SEP + self.get_name()

        return

    def get_nest_depth(self):
        """
        Obtain my full name. which is my name appended to my parent's name
        :return:
        """
        if self['path'] is None or self['path'] == self.PATH_SEP:
            return 0
        else:
            return self['path'].count(self.PATH_SEP)

    def set_trace(self, trace):
        self._trace = trace
        return

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        if not isinstance(parent, DataCore):
            raise TypeError("DataCore parent must be type:DataCore, not %s" % type(parent))
        self._parent = parent

    def set_template(self, value):
        # if value.get_attribute("class") , DataTemplate):
        #     raise TypeError("DataCore template must be type:DataTemplate, not %s" % type(value))
        self._template = value

    def get_index(self):
        """
        :return: the INDEX for this object in the core data base
        :rtype: int
        """
        return self['index']

    def set_index(self, value):
        """
        Set the INDEX for this object in the core data base

        :param value: the index
        :type value: int
        :rtype: None
        """
        if not isinstance(value, int):
            raise TypeError("DataCore.set_index() requires INT parameter")
        self['index'] = value

    def all_attrib_copy(self):
        return copy.copy(self._attrib)

    def get_attribute(self, name: str):
        """
        Get an object attribute, handling abstraction to any template
        :param name:
        :return:
        """
        if name in self._attrib:
            # then we have a 'local' instance value, so return it
            return self._attrib[name]

        if self._template is not None:
            # then see if our template has a value
            result = self._template.get_attrib(name)
            if result is not None:
                return result
            # else fall through

        # specialty attributes
        if name == 'display_name':
            # if no display name, use data name
            return self._attrib['data_name']

        # else just return None
        return None

    def set_private(self, value=True):
        """
        Set a local flag for 'private', meaning we don't expose for DATA updates

        :param value: whether this object is private or public
        :type value: bool
        """
        self._private = value

    @staticmethod
    def validate_name(value):
        """
        Validate (Convert & Test) the item name, return the name if okay, else throw an exception

        :param value: Morsel name
        :type value: str
        :return:
        """
        # confirm boils down to the unicode subset we support
        return validate_name(value)

    # manage the child list

    def add_child(self, child):
        """
        Add a child to our list

        :param child:
        :return:
        """
        # TODO - confirm is unique by full name?

        # add to our child list
        self._children_list.append(child)

        # obviously, this makes us the 'parent'
        child.set_parent(self)

        # refresh the full name, as it likely changed
        child.refresh_full_name()

        # add to the 'by name' keyed dict, adding the dict is None
        if self._children_keyed is None:
            self._children_keyed = dict()
        self._children_keyed[child.get_full_name()] = child
        return True

    def find_child(self, full_name: str, list_scan=False):
        """
        Scan our child list for the named child

        :param full_name:
        :return:
        """
        full_name = full_name.lower()

        if self._children_keyed is not None:
            if full_name in self._children_keyed:
                return self._children_keyed[full_name]

        # if not found, then maybe full_name is not full, so return FIRST simple match
        if list_scan:
            for child in self._children_list:
                if child['data_name'] == full_name:
                    return child
        return None

    # def build_list_names(self, root=None, recursive=True):
    #     """
    #     Return a list of DataList names only
    #
    #     :param root:
    #     :type root: str
    #     :return:
    #     :rtype: list of str
    #     """
    #     if root is None:
    #         root = ''
    #
    #     names = []
    #     for child in self._children:
    #         if child.get_role() == self.ROLE_LIST:
    #             if self._parent is None:
    #                 # then skip our name, for the root doesn't exist
    #                 name = root + self.PATH_SEP + child.get_name()
    #             else:  # include our name
    #                 name = root + self.PATH_SEP + self.get_name() + self.PATH_SEP + child.get_name()
    #             names.crc_append(name)
    #
    #             if recursive:
    #                 names.extend(child.build_list_names(root))
    #         # we skip the DataObjects in the list
    #
    #     return names

    def build_object_names(self, root=None, recursive=True):
        """
        Return a list of DatObject names only

        :param root:
        :type root: str
        :return:
        :rtype: list of str
        """
        if root is None:
            root = ''

        names = []
        for child in self._children_list:
            name = root + self.PATH_SEP + self.get_name() + self.PATH_SEP + child.get_name()
            names.append(name)

            # we skip the DataList in the list
            if recursive and len(child) > 0:
                if self._parent is None:
                    # then skip our name
                    my_root = root
                else:  # include out name
                    my_root = root + self.PATH_SEP + self.get_name()
                names.extend(child.build_object_names(my_root))

        return names

    def import_child_list(self, source):
        """
        Given a list of Python dicts, representing a list of sub-objects, allocate and load them

        :type source: list
        """
        if source is not None and len(source):
            from data.boot_database import create_data_core_object
            for child in source:
                # allocate the object, import the base config from source
                create_data_core_object(child, self)
        return

    # def import_child_one(self, source, data_base=None):
    #     """
    #     Given one Python dicts, a sub-objects, allocate and load them
    #
    #     :param source: object config like {"class": "DataObject", "data_type": "num", "name": "min", "uom": "gal"}
    #     :type source: list
    #     :rtype: DataCore
    #     """
    #     assert isinstance(source, types.DictionaryType)
    #
    #     if data_base is None:
    #         data_base = self.get_core_data_base()
    #
    #     # add this object to the main database
    #     self['path'] = data_base.add_to_data_base(value)
    #
    #     return value

    def export_json(self, pass_in=None):
        """
        Dump self as a JSON object

        :param pass_in: the elements from others
        :type pass_in: dict
        :return:
        :rtype: str
        """
        if pass_in is None:
            result = dict()
        else:
            if not isinstance(pass_in, dict):
                raise TypeError("DataCore.export_json() requires DICT input")
            result = copy.copy(pass_in)

        if self._children_list is None or len(self._children_list) == 0:
            # then there is no child list
            child_config = None

        else:  # create the list of children
            child_config = '"child": ['
            for child in self._children_list:
                child_config += child.export_json() + ', '
            child_config = child_config[:-2] + ']'

        for key in self._required_keys:
            if (key in self._attrib) and (key not in result) and (self[key] is not None):
                # only add keys NOT already there (allow sub-class to place as special)
                result[key] = self[key]

        # for key in self._optional_keys:
        #     if (key in self._attrib) and (key not in result) and (self[key] is not None):
        #         # only add keys NOT already there (allow sub-class to place as special)
        #         result[key] = self[key]

        for key in ('class', 'data_name'):
            # pop these off to make JSON cleaner, with class and name at front
            if key in result:
                del result[key]

        # we keep class/name out of result to allow for a cleaner JSON with those two at the head
        if len(result):
            json_out = json.dumps(result)
            # print '1st:' + json
            # then we had something
            json_out = '{"class": "%s", "name": "%s", ' % (self['class'], self['data_name']) + json_out[1:]

        else:  # we had nothing in result, so was "{}"
            json_out = '{"class": "%s", "name": "%s"}' % (self['class'], self['data_name'])
        # print '2nd:' + json

        if child_config is not None:
            # then crc_append the child list config info
            json_out = json_out[:-1] + ', ' + child_config + '}'
            # print '3rd:' + json

        return json_out

    def import_json(self, source, strict=True):
        """
        Convert JSON object to Python, then import the object

        :param source: the JSON source
        :type source: str or dict
        :return: any UNPROCESSED keys from source, as Python dict().
        :rtype: dict
        """
        if not isinstance(source, dict):
            # if not dictionary, assume is JSON string, convert to Python

            if not isinstance(source, str):
                raise TypeError("DataCore.import_json() requires str input")

            source = json.loads(source)
            # print 'import source:%s' % str(result)

        if strict:
            # confirm things like 'class' and 'data_name' exist
            for key in self._required_keys:
                if key not in source:
                    raise ValueError("DataCore.import_json() requires key:" + key)

            # convert, being strict, else be sloppy & allow any name
            source['data_name'] = self.validate_name(source['data_name'])

        return self.import_dict(source)

    def import_dict(self, source):
        """
        load/import self from a Python dictionary

        :param source: the python dict()
        :type source: dict
        :return: any UNPROCESSED keys from source, as Python dict().
        :rtype: dict
        """
        if not isinstance(source, dict):
            raise TypeError("DataCore.import_dict() requires dict input")

        # we need a deep copy, since we POP off consumed values, which might affect OTHER objects sharing a config
        source = copy.deepcopy(source)

        # print 'import:%s' % source['data_name']

        key = 'data_type'
        if key in source:
            # special handling for data-type, need to convert from JSON normal to internal type
            self[key] = data_type_import_from_json(source[key])
            del source[key]

        # copy over the optional keys
        for key in self._required_keys:
            if key in source:
                self[key] = source[key]
                del source[key]

        # copy over the optional keys
        for key in self._optional_keys:
            if key in source:
                self[key] = source[key]
                del source[key]

        # handle import of children (is recursive)
        key = 'child'
        if key in source:
            # then handle the children
            if not isinstance(source[key], list):
                raise TypeError("['child'] must be type list, not %s" % type(source[key]))
            self.import_child_list(source[key])

        # for child in self._children:
        #     child.refresh_full_name()

        return source

    def my_report(self, spacer=None):
        """
        return a list of report items

        :rtype: list
        """
        report = list()

        if spacer is None:
            spacer = ""
        line = spacer + "[%03d]" % self._attrib['index'] + " Type:{0}".format(self._attrib['class'])
        line += ", Name:\"{0}\"".format(self._attrib['data_name'])
        if 'path' in self._attrib:
            line += ", Full:\"{0}\"".format(self._attrib['path'])
        report.append(line)

        # print("Line:{0}".format(line))

        line = spacer + "  "
        if not len(self._children_list):
            pass
            # line += "Child Count: None"

        else:
            # then add the 'children'
            line = spacer + "  Child Count:%d" % len(self._children_list)
            report.append(line)
            for child in self._children_list:
                report.extend(child.my_report(spacer + "  "))
                pass

        return report


def create_single_data_core_instance(source, parent):
    """
    Given a Python dicts like this:
    # {"class": "DataObject", "data_type": "num", "name": "min", "value": 10, "uom": "gal"}

    Allocate the defined object, then import the rest of the dict. Do the imports in here to avoid circular
    import errors in DataCore object __init__

    :type source: dict
    :rtype: DataCore
    """

    assert isinstance(source, dict)

    class_name = source['class']
    if class_name == "DataObject":
        from data.data_object import create_data_object
        value = create_data_object(source['data_name'])

    elif class_name == "DataSetting":
        from data.data_setting import create_data_setting
        value = create_data_setting(source['data_name'])

    elif class_name == "DataTemplate":
        from data.data_template import create_data_template
        value = create_data_template(source['data_name'])

    else:
        raise ValueError("bad child['class'] in %s" % class_name)

    # add this object to our own child table
    parent.add_child(value)
    # print 'add:%s' % value['data_name']

    data_base = parent.get_core_data_base()

    # add this object to the main database
    value['path'] = data_base.add_to_data_base(value)

    # import the rest of the dict into the object
    value.import_dict(source)

    return value
