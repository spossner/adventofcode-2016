import re
import itertools


class Solution:
    def solve(self, data):
        if type(data) is not list:
            data = [data]
        cmds = [(c[0], int(c[1:])) for c in data]
        pos = (0, 0)
        vec = (0, 1)
        # N:   0,  1
        # E:   1,  0
        # S:   0, -1
        # W:  -1,  0

        visited = set()

        for dir, distance in cmds:
            if dir == 'R':
                vec = (vec[1], -vec[0])
            elif dir == 'L':
                vec = (-vec[1], vec[0])

            for i in range(distance):
                pos = (pos[0] + vec[0], pos[1] + vec[1])
                if pos in visited:
                    print(pos)
                    return abs(pos[0]) + abs(pos[1])
                visited.add(pos)

        return -1


if __name__ == '__main__':
    s = Solution()
    # assert s.solve([cmd.strip() for cmd in "R2, L3".split(',')]) == 5
    #assert s.solve([cmd.strip() for cmd in "R2, R2, R2".split(',')]) == 2
    # assert s.solve([cmd.strip() for cmd in "R5, L5, R5, R3".split(',')]) == 12
    assert s.solve([cmd.strip() for cmd in "R8, R4, R4, R8".split(',')]) == 4
    with open('01.txt') as f:
        print(s.solve([cmd.strip() for cmd in f.read().split(',')]))
