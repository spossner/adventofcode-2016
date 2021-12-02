import os
import sys


class Solution:
    def solve(self, data, width=50, height=6):
        if type(data) is not list:
            data = [data]

        grid = [[0]*width for _ in range(height)]

        for row in data:
            cmd = row[0:2]
            if cmd == 're':
                w, h = [int(a) for a in row.split(' ')[-1].split('x')]
                for y in range(h):
                    for x in range(w):
                        grid[y][x] = 1
            else:
                attr = row.split('=')
                pos = attr[0][-1]
                i, d = [int(a) for a in attr[1].split(' by ')]
                if pos == 'y':
                    # rotate row i by d
                    assert i >= 0 and i < height
                    assert d > 0 and d < width
                    print(row, grid[i], end=' -> ')
                    grid[i] = [*grid[i][width-d:], *grid[i][0:width-d]]
                    print(grid[i])
                else:
                    # rotate col i by d
                    assert i >= 0 and i < width
                    assert d > 0 and d < height
                    v = [row[i] for row in grid]
                    print(row, v, end=' -> ')
                    v = [*v[height - d:], *v[0:height - d]]
                    print(v)
                    for y in range(height):
                        grid[y][i] = v[y]
            for l in grid:
                print(''.join(['#' if i == 1 else ' ' for i in l]))
        total = 0
        for row in grid:
            total += sum(row)
        return total



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        print(s.solve(f.read().strip().splitlines(), 7, 3))

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip().splitlines()))