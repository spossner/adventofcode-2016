import re
import itertools


class Solution:
    def __init__(self):
        self.pad = (
            (None, None, 1, None, None),
            (None, 2, 3, 4, None),
            (5, 6, 7, 8, 9),
            (None, 'A', 'B', 'C', None),
            (None, None, 'D', None, None),
        )

    def solve(self, data):
        if type(data) is not list:
            data = [data]

        pos = (2, 0)  # start at 5

        for instr in data:
            for m in instr:
                if m == 'U':
                    pos = self.validate(pos, -1, 0)
                elif m == 'D':
                    pos = self.validate(pos, 1, 0)
                elif m == 'L':
                    pos = self.validate(pos, 0, -1)
                elif m == 'R':
                    pos = self.validate(pos, 0, 1)
            print(self.pad[pos[0]][pos[1]], end='')
        print()

    def validate(self, pos, dx, dy):
        if pos[0] + dx < 0 or pos[1] + dy < 0:
            return pos
        if pos[0] + dx >= len(self.pad) or self.pad[pos[0] + dx][pos[1]] is None:
            return pos
        if pos[1] + dy >= len(self.pad[0]) or self.pad[pos[0]][pos[1] + dy] is None:
            return pos
        return (pos[0]+dx, pos[1]+dy)

if __name__ == '__main__':
    s = Solution()
    with open('02-dev.txt') as f:
        s.solve(f.read().strip().splitlines())

    with open('02.txt') as f:
        s.solve(f.read().strip().splitlines())
