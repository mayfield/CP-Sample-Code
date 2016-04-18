__author__ = 'Lynn'


class Eoln(object):

    RAW = 'raw'
    CR = '<CR>'
    NL = '<NL>'
    CRNL = '<CR><NL>'

    def __init__(self):
        self.mode = self.NL
        return

    def set_mode(self, value):

        if value is None:
            value = 'raw'

        value = value.lower()

        if value in ('', 'raw', b'raw'):
            self.mode = self.RAW

        elif value in ('\r', b'\r', '<cr>'):
            self.mode = self.CR

        elif value in ('\n', b'\n', '<nl>'):
            self.mode = self.NL

        elif value in ('\r\n', b'\r\n', '<cr><nl>'):
            self.mode = self.CRNL

        else:
            raise ValueError("EOLN mode must be in set(None, '\\r', '\\n', '<CR><NL>'")

        return

    def process(self, data):
        """
        converts the data to the correct form

        :param data:
        :type data: bytes or str
        :return:
        """
        if self.mode == self.RAW:
            # for raw, just return exactly as is, one chunk in a list
            return data, False

        if data is None or len(data) == 0:
            # special case of no data
            return [], False

        # else we are doing to do some repacking, convert to string
        data = data.decode("utf-8")

        data_list = []

        if self.mode == self.CR:
            # do this the hard way, as we want to retain the <CR>

            data_line = ''
            for by in data:
                if by == '\n':
                    # discard any <NL>
                    continue
                # print("[{}] + [{}]".format(data_line, by))
                data_line += by
                if by == '\r':
                    data_list.append(data_line)
                    data_line = ''

            if len(data_line):
                data_list.append(data_line)
                # we have some 'left-over' stuff
                return data_list, False
            else:
                return data_list, True

        if self.mode == self.NL:
            # do this the hard way, as we want to retain the <NL>

            data_line = ''
            for by in data:
                if by == '\r':
                    # discard any <CR>
                    continue
                data_line += by
                if by == '\n':
                    data_list.append(data_line)
                    data_line = ''

            if len(data_line):
                # we have some 'left-over' stuff
                data_list.append(data_line)
                return data_list, False
            else:
                return data_list, True

        if self.mode == self.CRNL:
            # do this the hard way, as we want to retain the <CRNL>

            data_line = ''
            have_cr = False
            for by in data:
                if by == '\r':
                    have_cr = True
                    continue

                if by == '\n':
                    if have_cr:
                        data_line += '\r\n'
                        data_list.append(data_line)
                        have_cr = False
                        data_line = ''

                    # else:  discard an unexpected <NL>
                    continue

                if have_cr:
                    have_cr = False
                data_line += by

            if have_cr:
                # then special - is okay to have CR at end of block (if NL starts next, will be discarded)
                have_cr = False
                data_line += '\r\n'
                data_list.append(data_line)
                data_line = ''

            if len(data_line):
                data_list.append(data_line)
                # we have some 'left-over' stuff
                return data_list, False
            else:
                return data_list, True

        raise ValueError("bad mode!")

