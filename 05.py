import hashlib
import re
import itertools
from collections import defaultdict


class Solution:
    def solve(self, data):
        i = 0
        result = ''
        while len(result) < 8:
            word = f"{data}{i}"
            md5 = hashlib.md5(word.encode()).hexdigest()
            if md5[:5] == '00000':
                print(md5[5], end='')
                result = result + md5[5]
            i += 1
        print()
        return result


if __name__ == '__main__':
    s = Solution()
    assert s.solve('abc') == '18f47a30'
    print(s.solve('ojvtpuvg'))
