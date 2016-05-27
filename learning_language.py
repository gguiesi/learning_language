# -*- coding: utf-8 -*-

import datetime
import re

class Sub:
    def __init__(self, ini, end):
        self.ini = ini
        self.end = end
        self.l1 = []
        self.l2 = []
        self.counter = 0

    def add_l1(self, sub):
        self.l1.append(sub)

    def add_l2(self, sub):
        self.l2.append(sub)

    '''
    Return 0 if inside 1s tolerance == SAME
    1 if self.ini > other.ini == self.ini forward other.ini
    -1 if self.ini < other.ini == self.ini behind other.ini
    '''
    def compare_ini(self, other):
        ini_list = [self.ini, other.ini]
        ini_list.sort()
        ini_delta = ini_list[1] - ini_list[0]
        if ini_delta.total_seconds() <= 1:
            return 0
        elif self.ini > other.ini:
            return 1
        else:
            return -1

    '''
        Return 0 if inside 1s tolerance == SAME
        1 if self.end > other.end == self.end forward other.end
        -1 if self.end < other.end == self.end behind other.end
        '''
    def compare_end(self, other):
        end_list = [self.end, other.end]
        end_list.sort()
        end_delta = end_list[1] - end_list[0]
        if end_delta.total_seconds() <= 1:
            return 0
        elif self.end > other.end:
            return 1
        else:
            return -1

    def __str__(self):
        format = '%s\r\n%s --> %s\r\n'

        ini = self.ini.strftime('%H:%M:%S,%f')[0:-3]
        end = self.end.strftime('%H:%M:%S,%f')[0:-3]

        l1_subs = '\r\n'.join(self.l1)
        l2_subs = '\r\n'.join(self.l2)

        return format % (self.counter, ini, end), l1_subs, l2_subs


class MergeSubtitle:
    SPLITTER = '''\r\n\r\n'''
    TIME_REGEX = r'\d{2}:\d{2}:\d{2},\d{3}'

    def __init__(self, filename1, filename2, merge_proportion=0.7):
        self.l1_data = self.__load_subtitles(filename1)
        self.l2_data = self.__load_subtitles(filename2)
        self.merge_proportion = merge_proportion

    def __load_subtitles(self, filename):
        f = open(filename)
        return f.read().split(MergeSubtitle.SPLITTER)

    def __parse_subs(self):
        l1_subs = self.__parse_sub(self.l1_data)
        l2_subs = self.__parse_sub(self.l2_data)
        return l1_subs, l2_subs

    def __parse_sub(self, subtitles):
        result = []
        while subtitles.__len__() > 0:
            data = subtitles.pop(0)
            # load init and end time
            try:
                ini, end = self.__parse_times(data)
            except IndexError:
                print 'ERROR on extract times:', data
                continue
            sub = Sub(ini, end)
            # load only text of legends
            # try:
            content = data.split('\r\n')
            sub.counter = content[0]
            sub.l1 = content[2:]
            # except IndexError:
            #     print 'Error on extract text:', data
            #     continue
            result.append(sub)
        return result

    def __parse_times(self, data):
        t = re.findall(MergeSubtitle.TIME_REGEX, data)
        ini = datetime.datetime.strptime(t[0], '%H:%M:%S,%f')
        end = datetime.datetime.strptime(t[1], '%H:%M:%S,%f')
        return ini, end

    '''
    Merge the two languages with a defined proportion.
    Ex. For a merge proportion of 0.7, the generated srt file will have 70 percent of L1 and 30 percent of L2
    '''
    def merge_subtitles(self):
        l1_subs, l2_subs = self.__parse_subs()
        count_l2 = 0
        count_l1 = 0
        while count_l1 < l1_subs.__len__():
            l1 = l1_subs[count_l1]
            l2 = l2_subs[count_l2]

            i = l1.compare_ini(l2)
            e = l1.compare_end(l2)
            # same interval
            if i == 0 and e == 0:
                l1.l2 = l1.l2 + l2.l1
                count_l2 += 1
                count_l1 += 1
            # l1.init forward l2.init, same end
            elif i > 0 and e == 0:
                print 'i > 0 and e == 0'
                l1.l2 = l1.l2 + [l2.l1.pop(0)]
                if l2.l1.__len__() == 0:
                    count_l2 += 1
                count_l1 += 1
            # l1.init behind l2.init, same end
            elif i < 0 and e == 0:
                print 'i < 0 and e == 0'
            # same init, l1.end forward l2.end
            elif i == 0 and e > 0:
                print 'i == 0 and e > 0'
                l1.l2 += [l2.l1.pop(0)]
                count_l1 += 1
                if len(l2.l1) < 1:
                    count_l2 += 1
            # same init, l1.end behind l2.end
            elif i == 0 and e < 0:
                print 'i == 0 and e < 0'
                l1.l2 += [l2.l1.pop(0)]
                count_l1 += 1
                if len(l2.l1) < 1:
                    count_l2 += 1
            else:
                print 'DUNNO:', i, e
                if i < 0:
                    count_l1 += 1
                else:
                    count_l2 += 1

        self.__generate_final_file(l1_subs)

    def __generate_final_file(self, subs, filename='final.srt'):
        f = open(filename, 'w')

        count_l1 = 0
        for sub in subs:
            r = count_l1 % 10
            ini, l1, l2 = sub.__str__()
            if len(sub.l2) > 0:
                count_l1 += 1
            if r > self.merge_proportion * 10 and len(sub.l2) > 0:
                # write l2
                f.write(ini + l2 + MergeSubtitle.SPLITTER)
            else:
                # write l1
                f.write(ini + l1 + MergeSubtitle.SPLITTER)

        f.close()

# TESTE CLASS
#path = '/Users/guiesi/Downloads/torrent/Penny.Dreadful.S03E04.720p.HDTV.x264-AVS[rarbg]/'
#merge_subs = MergeSubtitle(path + 'Penny.Dreadful.S03E04.720p.HDTV.x264-AVS.en.srt',
#                           path + 'Penny.Dreadful.S03E04.720p.HDTV.x264-AVS.pt.srt')
#merge_subs.merge_subtitles()
