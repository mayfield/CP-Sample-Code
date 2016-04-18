# File: data_sample.py
# Desc: a data sample with value, time-stamp, quality, reference to a template

# History:
#
# 1.0.0: 2015-Mar Lynn
#       * initial draft
#
#

"""\
The data samples:

"""

import time
import json

import common.quality as quality
# from data.data_template import DataTemplate

__version__ = "1.0.0"


class DataSample(object):

    def __init__(self):

        self.__value = None
        self._timestamp = 0
        self._quality = quality.QUALITY_MASK_VALID
        self._template = None
        return

    @staticmethod
    def code_name():
        return 'DataSample'

    @staticmethod
    def code_version():
        return __version__

    def __str__(self):
        if self._template is None:
            return 'Data:%s' % self.__value
        else:
            return self._template.get_string(self)

    # def __repr__(self):
    #     return "Status=0x%08X" % self._quality

    # the VALUE routines
    
    def get_value(self):
        """
        :return: the value of this sample
        :rtype: object
        """
        return self.__value

    def set_value(self, value, now, param=None):
        """
        Set a value - we need to isolate self.__value, as we need template to filter the setting.

        :param value: the proposed value
        :param now: the time to use in the sample (if None, use time.time())
        :type now: float
        :return: T if the value changed, else F if no change, else exception will be thrown
        :rtype: bool
        """
        # we start by clearing the 'old' quality data
        self._quality = quality.QUALITY_MASK_VALID

        if self._template is None:
            self.__value = value
        else:
            self.__value, quality_change = self._template.process_value(value, param)
            if quality_change:
                # then something changed in the quality bits
                self._quality |= quality_change

        self.set_timestamp(now)
        return True

    # the TIMESTAMP routines
    
    def get_timestamp(self):
        """
        :return: the time of this sample
        :rtype: float
        """
        return self._timestamp

    def get_timestamp_string(self):
        """
        :return: string of time of this sample
        :rtype: str
        """
        return time.strftime("Y-m-d H:M:S", time.gmtime(self._timestamp))

    def set_timestamp(self, value=None):
        """
        Set a value - we need to isolate self.__value, as we need template to filter the setting.

        :param value: the proposed value
        :return: the value if was set, else an exception will be thrown
        :rtype: unicode
        """
        if value is None:
            value = time.time()
        self._timestamp = value
        return

    # the TEMPLATE routines

    def get_template(self):
        """
        :return: the value of this sample
        :rtype: None or DataTemplate
        """
        return self._template

    def get_template_string(self):
        """
        :return: the value of this sample
        """
        if self._template is None:
            return None
        else:
            return self._template['name']

    def set_template(self, value):
        """
        Set a value - we need to isolate self.__value, as we need template to filter the setting.

        :param value: the proposed value
        :return: the value if was set, else an exception will be thrown
        :rtype: None
        """
        if isinstance(value, str):
            # then look up the template
            value = None

        self._template = value
        return

    def get_uom(self):
        if self._template is not None:
            return self._template.get_uom()
        return None

    # the QUALITY routines

    def get_quality(self):
        """
        :return: the quality value of this sample
        :rtype: int
        """
        return self._quality

    def get_quality_string(self):
        """
        :return: the quality value of this sample
        :rtype: int
        """
        return quality.all_bits_to_tag(self._quality)

    def clr_quality_bits(self, bits):
        """using bit-mask, clear bits"""
        self._quality &= ~bits
        self._quality |= quality.QUALITY_MASK_VALID

    def set_quality_bits(self, bits):
        """using bit-mask, set bits"""
        self._quality |= (bits | quality.QUALITY_MASK_VALID)

    def set_quality(self, bits):
        """completely set/replace value"""
        self._quality = (bits | quality.QUALITY_MASK_VALID)

    def export_dict(self, raw=True):
        """
        Dump self as a python dictionary
        :rtype: dict
        """
        result = dict()

        result['class'] = self.code_name()
        result['value'] = self.get_value()
        if raw:
            result['timestamp'] = self.get_timestamp()
            result['quality'] = self.get_quality()
            if self._template is not None:
                result['template'] = self.get_template()
        else:  # export as string
            result['timestamp'] = self.get_timestamp_string()
            result['quality'] = self.get_quality_string()
            if self._template is not None:
                result['template'] = self.get_template_string()
        return result

    def export_json(self, pass_in=None):
        """
        Dump self as a JSON object

        :param pass_in: the elements from others
        :type pass_in: dict
        :return:
        :rtype: str
        """
        if pass_in is not None and not isinstance(pass_in, dict):
            raise TypeError("%s.export_json() requires DICT input" % self.code_name())

        # fetch the values as strings
        result = self.export_dict(raw=False)
        return json.dumps(result)

    def import_json(self, source, strict=True):
        """
        Dump self as a JSON object

        :param source: the JSON source
        :return:
        :rtype: dict
        """
        if not isinstance(source, str):
            raise TypeError("%s.import_json() " % self.code_name() + "requires str input")

        # converts JSON to Python dictionary
        result = json.loads(source)

        if 'class' in result and result['class'] != self.code_name():
            raise ValueError("%s.import_json() " % self.code_name() + "rejected ['class'] value")

        if 'value' not in result:
            # don't overwrite a value passed in by derived class
            result['value'] = self.get_value()

        if 'timestamp' not in result:
            # don't overwrite a value passed in by derived class
            result['timestamp'] = self.get_timestamp()

        if 'unit' not in result:
            # don't overwrite a value passed in by derived class
            result['unit'] = self.get_uom()

        if 'quality' not in result:
            # don't overwrite a value passed in by derived class
            result['quality'] = self.get_quality()

        # if strict:
        #     # confirm things like 'role' and 'name' exist
        #     for key in self._required_keys:
        #         if key not in result:
        #             raise ValueError("%s.import_json() requires " % self.code_name() +
        #                              "key:" + key)
        #
        #     # convert
        #     result['name'] = self.validate_name(result['name'])
        #
        # if 'name' in result:
        #     self['name'] = result['name']

        return result
