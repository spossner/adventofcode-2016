import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy, copy

WAYS = (
    (0, -1), (0, 1), (-1, 0), (1, 0)
)
WAY_CHARS = 'UDLR'

class Solution:
    def solve(self, data, modified=False):
        width, height = 4, 4
        d = deque()
        d.append((data, '', (0, 0)))
        result = ''
        while len(d) > 0:
            for _ in range(len(d)):
                word, path, pos = d.popleft()
                if pos == (width - 1, height - 1):
                    if not modified:
                        return ''.join(path)
                    if len(path) > len(result):
                        result = path
                    continue
                doors = hashlib.md5(word.encode()).hexdigest()[:4]
                #print(pos, word, doors)
                for i in range(4):
                    #98 bis 102
                    if 98 <= ord(doors[i]) <= 102:
                        new_pos = (pos[0]+WAYS[i][0], pos[1]+WAYS[i][1])
                        if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height: # valid position?
                            new_path = path+WAY_CHARS[i]
                            d.append((f"{data}{new_path}", new_path, new_pos))

        return result


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    #print(s.solve('hijkl'))
    #print(s.solve('ihgpwlah'))
    # print(s.solve('kglvqrro'))
    # print(s.solve('ulqzkmiv'))
    # print(s.solve('pvhmgsws'))
    print(len(s.solve('ihgpwlah', True)))
    print(len(s.solve('kglvqrro', True)))
    print(len(s.solve('ulqzkmiv', True)))
    print(len(s.solve('pvhmgsws', True)))
