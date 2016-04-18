def parse_01():
    # first clean-up - split lines, append, etc

    def save_01(fh, line_save):
        """

        :param fh: the output file
        :type fh: file
        :param line_save:
        :type line_save: str
        :return:
        """
        if line_save[0:2] == 'c5':
            fh.write('\n')
        else:
            fh.write(' ')

        fh.write(line_save)
        print(line_save)

    fin = open("01_in.py", 'r')
    fout = open("02_in.py", 'w')

    for line in fin:
        if len(line) < 1:
            continue

        line = line.strip()

        offset = 1
        while offset > 0:
            offset = line.find('c5', 2)
            if offset > 1:
                print("pre:%s" % line)
                print("ofs:%d" % offset)
                # we found a 'second' c5, so break up
                pre = line[:offset]
                save_01(fout, pre)
                line = line[offset:]
            else:  # this is the first
                pass

        save_01(fout, line)

    fin.close()
    fout.close()


def parse_02():
    # second clean-up - convert to b''

    fin = open("01_in.py", 'r')
    fout = open("02_in.py", 'w')

    for line in fin:
        if len(line) < 1:
            continue

        line = line.strip()
        tokens = line.split()

        result = "b\'"
        for toks in tokens:
            result += "\\x" + toks

        result += "\'\n"
        print(result)
        fout.write(result)

    fin.close()
    fout.close()


def merge_03():
    # third clean-up - merge the two files

    fin_out = open("02_out.py", 'r')
    fin_in = open("02_in.py", 'r')
    fout = open("03_all.py", 'w')

    index = 0
    while True:
        line_out = fin_out.readline().strip()
        line_in = fin_in.readline().strip()

        if len(line_out) < 3:
            break

        result = "    (%d, " % index + line_out + ", " + line_in + "),\n"
        index += 1

        print(result)
        fout.write(result)

    fin_out.close()
    fin_in.close()
    fout.close()

merge_03()

