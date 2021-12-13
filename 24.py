import os
import sys
from collections import deque

WAYS = (
    (0, -1), (0, 1), (-1, 0), (1, 0)
)

class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        grid = data
        d = deque()
        start = None
        goals = []
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == '0':
                    start = (x, y)
                elif c.isnumeric():
                    goals.append(c)

        d.append((start, [], goals, 0))  # (x, y), seen, goals, #steps
        result = None
        while d:
            # self.dump(grid)
            for _ in range(len(d)):
                p, seen, open, steps = d.popleft()
                x, y = p
                if p in seen:
                    continue
                seen = [*seen, p]

                if grid[y][x] in open: # found one
                    open = [e for e in open if e != grid[y][x]]
                    seen = [] # can walk back now

                if not open: # found a solution
                    if result is None or steps < result:
                        result = steps
                        print(f"found a solution with {result} steps")
                        continue

                for dx, dy in WAYS:
                    nx = x+dx
                    ny = y+dy
                    if nx < 0 or ny < 0 or ny >= len(grid) or ny >= len(grid[0]):
                        continue
                    c = grid[ny][nx]
                    if c == '#': # wall
                        continue
                    d.append(((nx, ny), seen, open, steps+1))

        return result

    def dump(self, grid):
        for row in grid:
            print(row)
        print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip().splitlines()))
