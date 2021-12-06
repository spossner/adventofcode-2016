import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
            # Disc #2 has 19 positions; at time=0, it is at position 10.
        print(data)

        re_disc = re.compile('Disc #(\d) has (\d+) positions; at time=0, it is at position (\d+).');

        init_discs = [[1,0]]
        for line in data:
            disc = re_disc.match(line).groups()
            init_discs.append([int(disc[1]), int(disc[2])])
        if modified:
            init_discs.append([11, 0])

        t_button = 1
        while True:
            discs = deepcopy(init_discs)
            print(f"checking {t_button} in {discs}")
            for disc in discs:
                disc[1] = (disc[1] + t_button) % disc[0]
            t = t_button
            started = False
            c = None
            while not started or c is not None:
                # print(t, c, discs)
                if t == t_button:
                    started = True
                    c = 0 # drop capsule
                elif c is not None:
                    if discs[c][1] == 0:
                        c += 1 # drop to next disc
                        if c >= len(discs):
                            return t_button+1
                    else:
                        c = None # soar aways
                elif started:
                    break
                t += 1
                for disc in discs[1:]:
                    disc[1] = (disc[1] + 1) % disc[0]
            t_button += 1
        return None


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    # with open(f'{script}.txt') as f:
    #      print(s.solve(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
         print(s.solve(f.read().strip().splitlines(), True))