# Test the 'health' template, for 0-100% values

import unittest

from data.data_sample import DataSample
from data.templates.template_health import TemplateHealth
from common.quality import QUALITY_MASK_VALID


class TestTemplateHealth(unittest.TestCase):

    def test_template(self):

        sample = DataSample()
        template = TemplateHealth()
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

    def test_sample(self):

        sample = DataSample()
        template = TemplateHealth()
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


if __name__ == '__main__':
    unittest.main()
