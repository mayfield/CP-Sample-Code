# Test the PARSE DURATION module

import unittest

import cp_lib.data.quality as qa


class TestQuality(unittest.TestCase):

    def test_one_bit_to_tag(self):

        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_DISABLE), 'dis')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_FAULT), 'flt')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_OFFLINE), 'ofl')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_OVER_RANGE), 'ovr')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_UNDER_RANGE), 'udr')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_NOT_INIT), 'N/A')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_QUAL_UNK), 'unq')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_QUAL_LOW), 'loq')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_MANUAL), 'man')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_CLAMP_HIGH), 'clh')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_CLAMP_LOW), 'cll')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_DIGITAL), 'dig')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_LO), 'low')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_LOLO), 'llo')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_ROC_NOR), 'roc')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_ROC_AB), 'rab')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_HI), 'hig')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_HIHI), 'hhi')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_DEV_NOR), 'dev')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_DEV_AB), 'dab')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_ABNORM), 'abn')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_RTNORM), 'rtn')
        self.assertEqual(qa.one_bit_to_tag(qa.QUAL_VALID), 'ok')

        # only 1 bit can be submitted
        with self.assertRaises(ValueError):
            qa.one_bit_to_tag(0xFF)

        # this is no match, 0 is not a valid bit
        with self.assertRaises(ValueError):
            qa.one_bit_to_tag(0)

        with self.assertRaises(ValueError):
            qa.one_bit_to_tag(None)

        with self.assertRaises(ValueError):
            qa.one_bit_to_tag(10.4)

        with self.assertRaises(ValueError):
            qa.one_bit_to_tag("what?")

        return

    def test_one_bit_to_name(self):

        self.assertEqual(qa.one_bit_to_name(qa.QUAL_DISABLE), 'disabled')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_FAULT), 'fault')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_OFFLINE), 'offline')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_OVER_RANGE), 'over-range')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_UNDER_RANGE),
                         'under-range')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_NOT_INIT),
                         'not-initialized')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_QUAL_UNK),
                         'unknown-quality')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_QUAL_LOW), 'low-quality')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_MANUAL), 'manual')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_CLAMP_HIGH), 'clamp-high')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_CLAMP_LOW), 'clamp-low')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_DIGITAL), 'digital')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_LO), 'low')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_LOLO), 'low-low')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_ROC_NOR), 'rate-of-change')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_ROC_AB),
                         'rate-of-change-abnorm')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_HI), 'high')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_HIHI), 'high-high')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_DEV_NOR), 'deviation')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_DEV_AB),
                         'deviation-abnormal')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_ABNORM), 'go-abnormal')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_RTNORM),
                         'return-to-normal')
        self.assertEqual(qa.one_bit_to_name(qa.QUAL_VALID), 'status-valid')

        # only 1 bit can be submitted
        with self.assertRaises(ValueError):
            qa.one_bit_to_name(0xFF)

        # this is no match, 0 is not a valid bit
        with self.assertRaises(ValueError):
            qa.one_bit_to_name(0)

        with self.assertRaises(ValueError):
            qa.one_bit_to_name(None)

        with self.assertRaises(ValueError):
            qa.one_bit_to_name(10.4)

        with self.assertRaises(ValueError):
            qa.one_bit_to_name("what?")

        return

    def test_all_bits_to_tag(self):

        bits = qa.QUAL_VALID
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=False), 'ok')
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=True), 'status-valid')

        bits = qa.QUAL_VALID | qa.QUAL_MANUAL
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=False), 'man')
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=True), 'manual')

        bits = qa.QUAL_VALID | qa.QUAL_MANUAL | \
            qa.QUAL_LO
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=False), 'man,low')
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=True), 'manual,low')

        bits = qa.QUAL_VALID | qa.QUAL_MANUAL | \
            qa.QUAL_LO
        bits |= qa.QUAL_ABNORM
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=False), 'man,low,abn')
        self.assertEqual(
            qa.all_bits_to_tag(bits, long_name=True),
            'manual,low,go-abnormal')

        # test lacking qa.QUAL_VALID
        with self.assertRaises(ValueError):
            qa.all_bits_to_tag(
                qa.QUAL_DISABLE, long_name=False)

        with self.assertRaises(ValueError):
            qa.all_bits_to_tag(
                qa.QUAL_DISABLE, long_name=True)

        return

    def test_clr_quality_tags(self):

        # test lacking qa.QUAL_VALID
        with self.assertRaises(TypeError):
            qa.clr_quality_tags(None, 'low')

        with self.assertRaises(TypeError):
            qa.clr_quality_tags(10.2, 'low')

        with self.assertRaises(TypeError):
            qa.clr_quality_tags('what?', 'low')

        bits = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        expect = qa.QUAL_VALID | qa.QUAL_MANUAL
        self.assertEqual(qa.clr_quality_tags(bits, 'low'), expect)

        bits = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        expect = qa.QUAL_VALID | qa.QUAL_LO
        self.assertEqual(qa.clr_quality_tags(bits, 'man'), expect)

        bits = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        expect = qa.QUAL_VALID
        self.assertEqual(qa.clr_quality_tags(bits, ('low', 'man')),
                         expect)

        bits = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        expect = qa.QUAL_VALID
        self.assertEqual(qa.clr_quality_tags(bits, ['low', 'man']),
                         expect)

        return

    def test_set_quality_tags(self):

        # test lacking qa.QUAL_VALID
        with self.assertRaises(TypeError):
            qa.set_quality_tags(None, 'low')

        with self.assertRaises(TypeError):
            qa.set_quality_tags(10.2, 'low')

        with self.assertRaises(TypeError):
            qa.set_quality_tags('what?', 'low')

        bits = 0
        expect = qa.QUAL_VALID | qa.QUAL_LO
        self.assertEqual(qa.set_quality_tags(bits, 'low'), expect)

        bits = qa.QUAL_VALID
        expect = qa.QUAL_VALID | qa.QUAL_LO
        self.assertEqual(qa.set_quality_tags(bits, 'low'), expect)

        bits = qa.QUAL_LO
        expect = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        self.assertEqual(qa.set_quality_tags(bits, 'man'), expect)

        bits = qa.QUAL_VALID
        expect = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        self.assertEqual(qa.set_quality_tags(bits, ('low', 'man')),
                         expect)

        bits = qa.QUAL_VALID
        expect = qa.QUAL_VALID | qa.QUAL_LO | qa.QUAL_MANUAL
        self.assertEqual(qa.set_quality_tags(bits, ['low', 'man']),
                         expect)

        return

    def test_tag_to_one_bit(self):

        bits = qa.QUAL_DISABLE
        tag = 'dis'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_FAULT
        tag = 'flt'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_OFFLINE
        tag = 'ofl'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_OVER_RANGE
        tag = 'ovr'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_UNDER_RANGE
        tag = 'udr'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_NOT_INIT
        tag = 'N/A'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_QUAL_UNK
        tag = 'unq'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_QUAL_LOW
        tag = 'loq'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_MANUAL
        tag = 'man'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_CLAMP_HIGH
        tag = 'clh'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_CLAMP_LOW
        tag = 'cll'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_DIGITAL
        tag = 'dig'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_LO
        tag = 'low'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_LOLO
        tag = 'llo'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_ROC_NOR
        tag = 'roc'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_ROC_AB
        tag = 'rab'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_HI
        tag = 'hig'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_HIHI
        tag = 'hhi'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_DEV_NOR
        tag = 'dev'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_DEV_AB
        tag = 'dab'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_ABNORM
        tag = 'abn'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_RTNORM
        tag = 'rtn'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        bits = qa.QUAL_VALID
        tag = 'ok'
        self.assertEqual(qa.QUALITY_SHORT_NAME[bits], tag)
        self.assertEqual(qa.QUALITY_TAG_TO_BIT[tag], bits)
        self.assertEqual(qa.tag_to_one_bit(tag), bits)

        with self.assertRaises(ValueError):
            qa.tag_to_one_bit(1)

        with self.assertRaises(ValueError):
            qa.tag_to_one_bit(10.3)

        with self.assertRaises(ValueError):
            qa.tag_to_one_bit(None)

        with self.assertRaises(ValueError):
            qa.tag_to_one_bit('what?')

        return


if __name__ == '__main__':

    # simple_check()

    unittest.main()
