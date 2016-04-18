"""
Helper to parse and display the day-of-week where 0 to 6 maps to Mon to Sun
"""

__version__ = "1.0.0"

# History:
#
# 1.0.0: 2015-Apr Lynn
#        * initial rewrite
#

DOW_CODE_TO_NAME = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

# note that T and S are ambiguous, so we can't use
DOW_NAME_TO_CODE = {
    'm  ': 0,
    'mo ': 0,
    'mon': 0,
    # 'T' for Tuesday is ambiguous, so NOT supported
    'tu ': 1,
    'tue': 1,
    'w  ': 2,
    'we ': 2,
    'wed': 2,
    # 'T' for Thursday is ambiguous, so NOT supported
    'th ': 3,
    'thu': 3,
    'f  ': 4,
    'fr ': 4,
    'fri': 4,
    # 'S' for Saturday is ambiguous, so NOT supported
    'sa ': 5,
    'sat': 5,
    # 'S' for Sunday is ambiguous, so NOT supported
    'su ': 6,
    'sun': 6,
}


def day_of_week_string_to_int(dow):
    """
    Given a string name like 'Mon' or 'monday', convert to day-of-week in
    range 0 to 6

    :param dow: the day-of-week as like 'Mon' or 'Monday'
    :type dow: str or int
    :return:
    """
    if isinstance(dow, int):
        # a simple short-cut, if already 0 to 6
        if 0 <= dow <= 6:
            return dow
        raise ValueError("requires STRING param or INT in range 0 to 6")

    if isinstance(dow, bytes):
        # make bytes into string
        dow = dow.decode()

    if not isinstance(dow, str):
        raise TypeError("requires STRING param, not %s" % type(dow))

    # force lower case & 3 chars. 'Monday' becomes 'mon', 'Th' becomes 'Th '
    dow = dow.lower() + '   '
    dow = dow[:3]

    # will throw KeyError if not a valid day-of-week
    return DOW_NAME_TO_CODE[dow]


def day_of_week_int_to_string(dow):
    """
    Given a number 0 to 6, return as on of
    ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] or error

    :param dow: the day-of-week, as 0-6 for Mon to Sun
    :type dow: int or str
    :return:
    """
    # raises IndexError if a bad day-of-week value
    if 0 <= dow <= 6:
        return DOW_CODE_TO_NAME[dow]
    # we don't want dow[-1] to work!
    raise IndexError("requires values from 0 to 6, not %s" % dow)


def day_of_week_list_to_int_list(dow_list):
    """
    Given a list like ['mon', 'wed', 'fri'], convert to [0, 2, 4]

    List is NOT sorted, in case you might want some day-of-week priority
    implied by order

    :param dow_list: a list of names
    :type dow_list: list or tuple
    :return:
    :rtype: list of int
    """
    if type(dow_list) not in (tuple, list):
        raise TypeError("requires LIST param, not %s" % type(dow_list))

    result = list()
    for one_day in dow_list:
        result.append(day_of_week_string_to_int(one_day))

    return result
