# Test the DATA_TEMPLATE for temperature

import unittest

from data.templates.conversion_clamps import ConversionClampLow, QUALITY_MASK_CLAMP_LOW, QUALITY_MASK_UNDER_RANGE, \
    ConversionClampHigh, QUALITY_MASK_CLAMP_HIGH, QUALITY_MASK_OVER_RANGE


class TestConversionClamps(unittest.TestCase):

    def test_clamp_mode_1(self):

        # test mode #1 is a clamp with a close dead region, such as if range is 0 to 100%, then for any value
        # from 2% or lower, clamp to 0%, or from 98% or higher, clamp at 100%
        # however, the range from 2 to 0% isn't a clamp quality
        # logger.info('test Conversion Clamp() with Low clamps, mode #1')
        # logger.info(' is if _output < value < _upper, then set to _output, but quality is zero/unaffected')

        test_output = 20
        test_upper = 25
        clamp_low = ConversionClampLow(param=test_output)
        clamp_low.set_upper_value(test_upper)

        result_value, result_quality = clamp_low.convert(0)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)
        # QUALITY_MASK_VALID is not added, as this is 'change in quality', not a full quality value

        result_value, result_quality = clamp_low.convert(19)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(20)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(21)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(22)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(23)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(24)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(25)
        self.assertEqual(result_value, 25)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(26)
        self.assertEqual(result_value, 26)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(79)
        self.assertEqual(result_value, 79)
        self.assertEqual(result_quality, 0)

        test_output = 80
        test_lower = 75

        clamp_high = ConversionClampHigh(param=test_output)
        clamp_high.set_lower_value(test_lower)

        result_value, result_quality = clamp_high.convert(23)
        self.assertEqual(result_value, 23)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(74)
        self.assertEqual(result_value, 74)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(75)
        self.assertEqual(result_value, 75)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(76)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(77)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(78)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(79)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(80)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(81)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(99)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        return

    def test_clamp_mode_2(self):

        # test mode #2 is a simple clamp, such as if range is 0 to 100%, then clamp at 0% or below to 0%
        # or clamp at 100% or above at 100%
        # logger.info('test Conversion Clamp() with Low clamps, mode #2')
        # logger.info(' if value < _output, _lower is None, set to _output, return quality as QUALITY_MASK_CLAMP_LOW')

        test_low = 20
        clamp_low = ConversionClampLow(param=test_low)

        result_value, result_quality = clamp_low.convert(0)
        self.assertEqual(result_value, test_low)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(19)
        self.assertEqual(result_value, test_low)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(20)
        self.assertEqual(result_value, test_low)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(23)
        self.assertEqual(result_value, 23)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(79)
        self.assertEqual(result_value, 79)
        self.assertEqual(result_quality, 0)

        # logger.info('test Conversion Clamp() with High clamps, mode #2')
        # logger.info(' if value < _output, _upper is None, set to _output, return quality as QUALITY_MASK_CLAMP_HI')

        test_high = 80
        clamp_high = ConversionClampHigh(param=test_high)

        result_value, result_quality = clamp_high.convert(23)
        self.assertEqual(result_value, 23)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(79)
        self.assertEqual(result_value, 79)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(80)
        self.assertEqual(result_value, test_high)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(81)
        self.assertEqual(result_value, test_high)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(99)
        self.assertEqual(result_value, test_high)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        return

    def test_clamp_mode_3_4(self):

        # mode 3 only clamps for a limited distance, so like from -5 to 0 becomes 0%. Below -5% remains unchanged
        # which may allow better remote error detection

        # mode 4 adds

        # logger.info('test Conversion Clamp() with Low clamps, mode #3')
        # logger.info(' if _lower < value < _output, then set to _output, and return quality as QUALITY_MASK_CLAMP_LOW')
        # logger.info('test Conversion Clamp() with Low clamps, mode #4')
        # logger.info(' if value < _lower, then leave value unchanged, but set QUALITY_MASK_UNDER_RANGE')

        test_output = 20
        test_lower = 15

        clamp_low = ConversionClampLow(param=test_output)
        clamp_low.set_lower_value(test_lower)

        result_value, result_quality = clamp_low.convert(0)
        self.assertEqual(result_value, 0)
        self.assertEqual(result_quality, QUALITY_MASK_UNDER_RANGE)

        result_value, result_quality = clamp_low.convert(14)
        self.assertEqual(result_value, 14)
        self.assertEqual(result_quality, QUALITY_MASK_UNDER_RANGE)

        result_value, result_quality = clamp_low.convert(15)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(16)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(17)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(18)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(19)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_LOW)

        result_value, result_quality = clamp_low.convert(20)
        self.assertEqual(result_value, 20)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(23)
        self.assertEqual(result_value, 23)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_low.convert(79)
        self.assertEqual(result_value, 79)
        self.assertEqual(result_quality, 0)

        # logger.info('test Conversion Clamp() with High clamps, mode #3')
        # logger.info(' if _output < value < _upper, then set to _output, and return quality as QUALITY_MASK_CLAMP_HI')
        # logger.info('test Conversion Clamp() with High clamps, mode #4')
        # logger.info(' if value > _upper, then leave value unchanged, but set QUALITY_MASK_OVER_RANGE')

        test_output = 80
        test_upper = 85
        clamp_high = ConversionClampHigh(param=test_output)
        clamp_high.set_upper_value(test_upper)

        result_value, result_quality = clamp_high.convert(23)
        self.assertEqual(result_value, 23)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(79)
        self.assertEqual(result_value, 79)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(80)
        self.assertEqual(result_value, 80)
        self.assertEqual(result_quality, 0)

        result_value, result_quality = clamp_high.convert(81)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(82)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(83)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(84)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(81)
        self.assertEqual(result_value, test_output)
        self.assertEqual(result_quality, QUALITY_MASK_CLAMP_HIGH)

        result_value, result_quality = clamp_high.convert(86)
        self.assertEqual(result_value, 86)
        self.assertEqual(result_quality, QUALITY_MASK_OVER_RANGE)

        result_value, result_quality = clamp_high.convert(99)
        self.assertEqual(result_value, 99)
        self.assertEqual(result_quality, QUALITY_MASK_OVER_RANGE)

        return


if __name__ == '__main__':
    unittest.main()
