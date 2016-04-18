__author__ = 'LLinse'


class DataRefresh(object):

    RATE_LIST_STR = ['1 hr', '3 hr', '6 hr', '12 hr', '1 day', '7 day', '14 day', '28 day', '1 mon']

    # set to TRUE to force rates to ve exact, else we round down
    EXACT_RATES = False

    def __init__(self):
        self.__refresh_lists = []
        for x in self.RATE_LIST_STR:
            self.__refresh_lists[x] = []
        return

    def add_data_object(self, data, rate):
        """
        Submit a data object, and a rate.
        :param data:
        :param rate:
        :type rate: str
        :return:
        """

        # convert the rate to a refresh list
        if rate not in self.RATE_LIST_STR:
            raise ValueError("Data refresh rate {0} is not in fixed list".format(rate))

        rate_index = self.RATE_LIST_STR.find()

