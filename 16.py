import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy, copy


class Solution:
    def solve(self, data, n, modified=False):
        while len(data) < n:
            tail = ''.join('1' if c == '0' else '0' for c in data[::-1])
            data = f"{data}0{tail}"
        data = data[:n]
        # print(data)

        chk = data
        while len(chk) % 2 == 0:
            result = []
            for i in range(0, len(chk), 2):
                result.append('1' if chk[i] == chk[i+1] else '0')
            chk = ''.join(result)
            #print(chk)

        return chk


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    print(s.solve('10000', 20))

    print(s.solve('10001110011110000', 272))
    print(s.solve('10001110011110000', 35651584))