# Test the DATA_TEMPLATE for temperature

import unittest

from data.data_sample import DataSample
from data.templates.template_temperature import TemplateTemperature
from data.templates.conversion_clamps import ConversionClampLow, QUALITY_MASK_CLAMP_LOW, \
    ConversionClampHigh, QUALITY_MASK_CLAMP_HIGH
from common.quality import QUALITY_MASK_VALID


class TestTemplateTemperature(unittest.TestCase):

    def test_template_degf(self):

        sample = DataSample()
        template = TemplateTemperature()
        template.set_degf(True)
        sample.set_template(template)

        self.assertEqual(sample.get_uom(), "F")

        sample.set_value(23, None)
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23)
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23, "f")
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23, "F")
        self.assertEqual(str(sample), "23 F")

        # template 'conversion' function ignores unknown tags
        sample.set_value(23, "happy")
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23, "c")
        self.assertEqual(str(sample), "73 F")

        sample.set_value(23, "C")
        self.assertEqual(str(sample), "73 F")

        sample.set_value(23, "degc")
        self.assertEqual(str(sample), "73 F")

        sample.set_value(23, "DegC")
        self.assertEqual(str(sample), "73 F")

        # confirm the round-down
        sample.set_value(23.3, None)
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23.3, "F")
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23.3, "happy")
        self.assertEqual(str(sample), "23 F")

        sample.set_value(23.3, "C")
        self.assertEqual(str(sample), "74 F")

        # confirm the round-up
        sample.set_value(23.8, None)
        self.assertEqual(str(sample), "24 F")

        sample.set_value(23.8, "F")
        self.assertEqual(str(sample), "24 F")

        sample.set_value(23.8, "happy")
        self.assertEqual(str(sample), "24 F")

        sample.set_value(23.8, "C")
        self.assertEqual(str(sample), "75 F")

        return

    def test_template_degc(self):

        sample = DataSample()
        template = TemplateTemperature()
        template.set_degf(False)
        sample.set_template(template)

        self.assertEqual(sample.get_uom(), "C")

        sample.set_value(23, None)
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23)
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23, "f")
        self.assertEqual(str(sample), "-5 C")

        sample.set_value(23, "F")
        self.assertEqual(str(sample), "-5 C")

        sample.set_value(23, "degf")
        self.assertEqual(str(sample), "-5 C")

        sample.set_value(23, "DegF")
        self.assertEqual(str(sample), "-5 C")

        # template 'conversion' function ignores unknown tags
        sample.set_value(23, "happy")
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23, "c")
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23, "C")
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23, "degc")
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23, "DegC")
        self.assertEqual(str(sample), "23 C")

        # confirm the round-down
        sample.set_value(23.3, None)
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23.3, "F")
        self.assertEqual(str(sample), "-5 C")

        sample.set_value(23.3, "happy")
        self.assertEqual(str(sample), "23 C")

        sample.set_value(23.3, "C")
        self.assertEqual(str(sample), "23 C")

        # confirm the round-up
        sample.set_value(23.8, None)
        self.assertEqual(str(sample), "24 C")

        sample.set_value(23.8, "F")
        self.assertEqual(str(sample), "-5 C")

        sample.set_value(23.8, "happy")
        self.assertEqual(str(sample), "24 C")

        sample.set_value(23.8, "C")
        self.assertEqual(str(sample), "24 C")

        return

    def test_template_precision(self):

        sample = DataSample()
        template = TemplateTemperature()
        sample.set_template(template)

        template.set_degf(False)
        template.set_precision(0.01)

        self.assertEqual(sample.get_uom(), "C")

        sample.set_value(23.123, None)
        self.assertEqual(str(sample), "23.12 C")

        sample.set_value(23.124, 'F')
        self.assertEqual(str(sample), "-4.93 C")

        sample.set_value(23.578, 'f')
        self.assertEqual(str(sample), "-4.68 C")

        # template 'conversion' function ignores unknown tags
        sample.set_value(23.456, 'happy')
        self.assertEqual(str(sample), "23.46 C")

        sample.set_value(23.1, 'c')
        self.assertEqual(str(sample), "23.10 C")

        sample.set_value(23.3, 'C')
        self.assertEqual(str(sample), "23.30 C")

        sample.set_value(23.3, None)
        self.assertEqual(str(sample), "23.30 C")

        sample.set_value(23.3, "F")
        self.assertEqual(str(sample), "-4.83 C")

        sample.set_value(23.3333, "C")
        self.assertEqual(str(sample), "23.33 C")

        sample.set_value(23.8, None)
        self.assertEqual(str(sample), "23.80 C")

        sample.set_value(23.8, "F")
        self.assertEqual(str(sample), "-4.56 C")

        sample.set_value(23.8888, "C")
        self.assertEqual(str(sample), "23.89 C")

        return

    def test_template_clamps(self):

        # these are the low/high clamps
        test_low = 20
        test_high = 80

        sample = DataSample()
        template = TemplateTemperature()
        sample.set_template(template)

        template.add_conversion(ConversionClampLow(param=test_low))
        template.add_conversion(ConversionClampHigh(param=test_high))

        sample.set_value(0.0)
        self.assertEqual(sample.get_value(), 20)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID | QUALITY_MASK_CLAMP_LOW)

        sample.set_value(19.0)
        self.assertEqual(sample.get_value(), 20)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID | QUALITY_MASK_CLAMP_LOW)

        sample.set_value(20.0)
        self.assertEqual(sample.get_value(), 20)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID)

        sample.set_value(23.123)
        self.assertEqual(sample.get_value(), 23)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID)

        sample.set_value(23.823)
        self.assertEqual(sample.get_value(), 24)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID)

        sample.set_value(79.0)
        self.assertEqual(sample.get_value(), 79)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID)

        sample.set_value(80.0)
        self.assertEqual(sample.get_value(), 80)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID)

        sample.set_value(81.0)
        self.assertEqual(sample.get_value(), 80)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID | QUALITY_MASK_CLAMP_HIGH)

        sample.set_value(99.9)
        self.assertEqual(sample.get_value(), 80)
        self.assertEqual(sample.get_quality(), QUALITY_MASK_VALID | QUALITY_MASK_CLAMP_HIGH)

        return


if __name__ == '__main__':
    unittest.main()
