import unittest

from cp_lib.data.day_of_week import day_of_week_string_to_int, \
    day_of_week_int_to_string, day_of_week_list_to_int_list


class TestDayOfWeek(unittest.TestCase):

    def test_dow_string_to_int(self):

        self.assertEqual(day_of_week_int_to_string(0), 'mon')
        self.assertEqual(day_of_week_int_to_string(0).capitalize(), 'Mon')
        self.assertEqual(day_of_week_int_to_string(0).upper(), 'MON')

        self.assertEqual(day_of_week_string_to_int('m'), 0)
        self.assertEqual(day_of_week_string_to_int('M'), 0)
        self.assertEqual(day_of_week_string_to_int('mo'), 0)
        self.assertEqual(day_of_week_string_to_int('Mo'), 0)
        self.assertEqual(day_of_week_string_to_int('mO'), 0)
        self.assertEqual(day_of_week_string_to_int('MO'), 0)
        self.assertEqual(day_of_week_string_to_int('mon'), 0)
        self.assertEqual(day_of_week_string_to_int('Mon'), 0)
        self.assertEqual(day_of_week_string_to_int('mOn'), 0)
        self.assertEqual(day_of_week_string_to_int('MON'), 0)
        self.assertEqual(day_of_week_string_to_int('monday'), 0)
        self.assertEqual(day_of_week_string_to_int('MONDAY'), 0)
        # note this routine is NOT very fussy - only looks at first 3 chars
        self.assertEqual(day_of_week_string_to_int('MONDAY but not yet!'), 0)

        self.assertEqual(day_of_week_int_to_string(1), 'tue')
        self.assertEqual(day_of_week_string_to_int('tu'), 1)
        self.assertEqual(day_of_week_string_to_int('tue'), 1)
        self.assertEqual(day_of_week_string_to_int('tuesday'), 1)
        self.assertEqual(day_of_week_string_to_int('tue-funky'), 1)

        self.assertEqual(day_of_week_int_to_string(2), 'wed')
        self.assertEqual(day_of_week_string_to_int('w'), 2)
        self.assertEqual(day_of_week_string_to_int('we'), 2)
        self.assertEqual(day_of_week_string_to_int('wed'), 2)
        self.assertEqual(day_of_week_string_to_int('wednesday'), 2)

        self.assertEqual(day_of_week_int_to_string(3), 'thu')
        self.assertEqual(day_of_week_string_to_int('th'), 3)
        self.assertEqual(day_of_week_string_to_int('thu'), 3)
        self.assertEqual(day_of_week_string_to_int('thurs'), 3)
        self.assertEqual(day_of_week_string_to_int('thursday'), 3)

        self.assertEqual(day_of_week_int_to_string(4), 'fri')
        self.assertEqual(day_of_week_string_to_int('f'), 4)
        self.assertEqual(day_of_week_string_to_int('fr'), 4)
        self.assertEqual(day_of_week_string_to_int('fri'), 4)
        self.assertEqual(day_of_week_string_to_int('friday'), 4)

        self.assertEqual(day_of_week_int_to_string(5), 'sat')
        self.assertEqual(day_of_week_string_to_int('sa'), 5)
        self.assertEqual(day_of_week_string_to_int('sat'), 5)
        self.assertEqual(day_of_week_string_to_int('saturday'), 5)

        self.assertEqual(day_of_week_int_to_string(6), 'sun')
        self.assertEqual(day_of_week_string_to_int('su'), 6)
        self.assertEqual(day_of_week_string_to_int('sun'), 6)
        self.assertEqual(day_of_week_string_to_int('sunday'), 6)

        with self.assertRaises(IndexError):
            day_of_week_int_to_string(-1)

        with self.assertRaises(IndexError):
            day_of_week_int_to_string(7)

        with self.assertRaises(KeyError):
            # 'T' and 'S' are ambiguous
            day_of_week_string_to_int('t')

        with self.assertRaises(KeyError):
            day_of_week_string_to_int('T')

        with self.assertRaises(KeyError):
            # 'T' and 'S' are ambiguous
            day_of_week_string_to_int('s')

        with self.assertRaises(KeyError):
            day_of_week_string_to_int('S')

        return

    def test_dow_list(self):

        self.assertEqual(day_of_week_list_to_int_list([]), [])
        self.assertEqual(day_of_week_list_to_int_list(['mon']), [0])
        self.assertEqual(day_of_week_list_to_int_list(['tue']), [1])
        self.assertEqual(day_of_week_list_to_int_list(['wed']), [2])
        self.assertEqual(day_of_week_list_to_int_list(['thu']), [3])
        self.assertEqual(day_of_week_list_to_int_list(['fri']), [4])
        self.assertEqual(day_of_week_list_to_int_list(['sat']), [5])
        self.assertEqual(day_of_week_list_to_int_list(['sun']), [6])

        self.assertEqual(day_of_week_list_to_int_list(
            ['Mon', 'Wed', 'Fri']), [0, 2, 4])
        self.assertEqual(day_of_week_list_to_int_list(
            ('Mon', 'Wed', 'Fri')), [0, 2, 4])
        self.assertEqual(day_of_week_list_to_int_list(
            ['M', 'W', 'F']), [0, 2, 4])
        self.assertEqual(day_of_week_list_to_int_list(
            ['Monday', 'Wed', 'Friday']), [0, 2, 4])
        self.assertEqual(day_of_week_list_to_int_list(
            ['Mon', 'tue', 'Wed', 'Thu', 'Fri']), [0, 1, 2, 3, 4])
        self.assertEqual(day_of_week_list_to_int_list(
            ['Fri', 'Wed', 'Mon']), [4, 2, 0])
        self.assertEqual(day_of_week_list_to_int_list(
            ['Sat', 'Sun']), [5, 6])

        # technically, this is a side-effect, but it works and allows one
        # to attempt to re-calc a 2nd time
        self.assertEqual(day_of_week_list_to_int_list([0, 2, 4]), [0, 2, 4])

        with self.assertRaises(KeyError):
            # fails if ANY of the values are bad
            day_of_week_list_to_int_list(['Mon', 'Cat', 'Fri'])

        with self.assertRaises(TypeError):
            day_of_week_list_to_int_list(0)

        with self.assertRaises(TypeError):
            day_of_week_list_to_int_list('mon')

if __name__ == '__main__':
    unittest.main()
