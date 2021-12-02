import hashlib
import re
import itertools
from collections import defaultdict


class Solution:
    def solve(self, data):
        i = 0
        result = [None] * 8
        while None in result:
            word = f"{data}{i}"
            md5 = hashlib.md5(word.encode()).hexdigest()
            if md5[:5] == '00000':
                pos = ord(md5[5]) - 48
                if pos < 8 and result[pos] is None:
                    result[pos] = md5[6]
                    print(result)
            i += 1
        return ''.join(result)


if __name__ == '__main__':
    s = Solution()
    #assert s.solve('abc') == '05ace8e3'
    print(s.solve('ojvtpuvg'))
