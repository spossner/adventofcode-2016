import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy

TRAPS = ['^^.', '.^^', '^..', '..^']

class Solution:
    def solve(self, data, n=3, modified=False):
        data = f".{data}."
        rows = [data]
        print(data)
        for i in range(1,n):
            row = rows[-1]
            new_row = ['.']
            for x in range(1,len(data)-1):
                new_row.append('^' if row[x-1:x+2] in TRAPS else '.')
            new_row.append('.')
            rows.append(''.join(new_row))
            # print(rows[-1])

        sum = 0
        for row in rows:
            sum += row.count('.') - 2 # substract first and last imaginary safe tile
        return sum


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    # with open(f'{script}.txt') as f:
    #      print(s.solve(f.read().strip().splitlines()))

    print(s.solve('..^^.'))
    print(s.solve('.^^.^.^^^^', 10))

    with open(f'{script}.txt') as f:
          print(s.solve(f.read().strip(), 40))

    with open(f'{script}.txt') as f:
          print(s.solve(f.read().strip(), 400000))