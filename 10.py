import os
import re
import sys
from collections import defaultdict


class Solution:
    def solve(self, data):
        re_value = re.compile("value (\d+) goes to bot (\d+)")
        re_bot = re.compile("bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")
        outputs = defaultdict(list)
        bots = defaultdict(list)
        cmds = {}
        for row in data:
            if row[:3] == 'val':
                m = re_value.match(row)
                assert m is not None
                bots[m.group(2)].append(int(m.group(1)))
            else:
                m = re_bot.match(row)
                assert m is not None
                cmds[m.group(1)] = ((m.group(2), m.group(3)), (m.group(4), m.group(5)))

        running = True
        while running:
            #print(bots)
            running = False
            for bot, chips in bots.items():
                if len(chips) == 2:
                    cmd = cmds[bot]
                    l, h = min(chips), max(chips)
                    if l == 17 and h == 61:
                        print(bot, chips, cmd)
                    if cmd[0][0] == 'bot':
                        bots[cmd[0][1]].append(l)
                    else:
                        outputs[cmd[0][1]].append(l)
                    if cmd[1][0] == 'bot':
                        bots[cmd[1][1]].append(h)
                    else:
                        outputs[cmd[1][1]].append(l)
                    bots[bot].clear()
                    running = True
                    break
        print(outputs)
        print(outputs['0'][0] * outputs['1'][0] * outputs['2'][0])


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        s.solve(f.read().strip().splitlines())

    with open(f'{script}.txt') as f:
        s.solve(f.read().strip().splitlines())
