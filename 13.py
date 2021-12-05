import os
import sys
from collections import deque


class Solution:
    def __init__(self, magic_numer):
        self.magic_number = magic_numer
        self.cache = {}
        self.grid = {}

    def is_wall(self, pos):
        x, y = pos
        x_x = self.cache.get((x, x))
        if x_x is None:
            x_x = x * x
            self.cache[(x, x)] = x_x
        y_y = self.cache.get((y, y))
        if y_y is None:
            y_y = y * y
            self.cache[(y, y)] = y_y
        x_y = self.cache.get((x, y))
        if x_y is None:
            x_y = x * y
            self.cache[(x, y)] = x_y
            self.cache[(y, x)] = x_y
        n = x_x + 3 * x + (x_y << 1) + y + y_y + self.magic_number
        b = "{0:b}".format(n)
        return b.count('1') & 1

    def solve(self, target):
        pos = (1, 1)
        d = deque()
        seen = set()
        d.append((pos, 0))
        # while d:
        for _ in range(50 + 1):
            for i in range(len(d)):
                p, steps = d.popleft()
                # if p == target:
                #    return steps
                if p in seen or p[0] < 0 or p[1] < 0:
                    continue
                seen.add(p)
                for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_pos = (p[0] + delta[0], p[1] + delta[1])
                    if not self.is_wall(new_pos):
                        d.append((new_pos, steps + 1))
        return len(seen)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution(10)
    print(s.solve((7, 4)))

    s = Solution(1350)
    print(s.solve((31, 39)))