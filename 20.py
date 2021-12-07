import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy
from itertools import chain


class Range:
    def __init__(self, a, b):
        self.start = min(a, b)
        self.end = max(a, b)

    @staticmethod
    def parse(s):
        a, b = [int(x) for x in s.split('-')]
        return Range(a, b)

    def __contains__(self, item):
        return self.start <= item.start and self.end >= item.end

    def __str__(self):
        return f"|{self.start},{self.end}|"

    #   10.....30
    # OTHER
    # 5....15
    #      15....35
    # 5----------35
    #     12.18
    def intersect(self, other):
        return \
            other.start <= self.start and other.end >= self.start or \
            other.start <= self.end and other.end >= self.end or \
            other.start <= self.start and other.end >= self.end or \
            other.start >= self.start and other.end <= self.end

    def merge(self, other):
        return Range(min(self.start, other.start), max(self.end, other.end))

    def __le__(self, other):
        return self.end <= other.start

    def __lt__(self, other):
        return self.end < other.start

    def __ge__(self, other):
        return self.start >= other.end

    def __gt__(self, other):
        return self.start > other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return str(self).__hash__()

    def __repr__(self):
        return self.__str__()


class Solution:
    def solve(self, data, modified=False):
        ranges = []
        for row in data:
            ranges.append(Range.parse(row))

        # for row in data:
        #     r = Range.parse(row)
        #     index = self.binarySearch(ranges,0,len(ranges)-1,r)
        #     if index is not None:
        #         ranges.insert(index, r)
        ranges.sort(key=lambda r: r.start)
        i = 0
        while i < len(ranges) - 1:
            r1 = ranges[i]
            r2 = ranges[i + 1]
            if r1.end + 1 == r2.start or r1.intersect(r2):
                ranges[i] = r1.merge(r2)
                ranges.pop(i+1)
            else:
                i += 1

        for i in range(len(ranges)-1):
            assert ranges[i].end + 1 < ranges[i+1].start

        result = 0
        for i in range(len(ranges)-1):
            r1 = ranges[i]
            r2 = ranges[i+1]
            if modified:
                result += (r2.start-r1.end-1)
            else:
                return r1.end + 1
        return result

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip().splitlines(), True))
