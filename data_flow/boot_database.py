
from data.data_object import create_data_object
from data.data_setting import DataSetting
from data.data_template import DataTemplate

__author__ = 'Lynn'


def create_data_core_object(source, parent=None):
    """
    Given a Python dicts like this:
    # {"class": "DataObject", "data_type": "num", "name": "min", "value": 10, "uom": "gal"}

    Allocate the defined object, then import the rest of the dict. Do the imports in here to avoid circular
    import errors in DataCore object __init__

    :type source: dict
    :rtype: DataCore
    """

    assert isinstance(source, dict)

    if parent is None:
        # then start a NEW database, with new root
        from data.data_base import DataBase

        parent = DataObject('root')
        base = parent.get_core_data_base()
        assert isinstance(base, DataBase)
        base.set_root(parent)

    class_name = source['class']
    if class_name == "DataObject":
        value = create_data_object(source['name'])

    elif class_name == "DataSetting":
        value = DataSetting(source['name'])

    elif class_name == "DataTemplate":
        value = DataTemplate(source['name'])

    else:
        raise ValueError("bad child['class'] in %s" % class_name)

    # add this object to our own child table
    parent.add_child(value)
    # print 'add:%s' % value['name']

    data_base = parent.get_core_data_base()

    # add this object to the main database
    value['path'] = data_base.add_to_data_base(value)

    # import the rest of the dict into the object
    value.import_dict(source)

    return value
