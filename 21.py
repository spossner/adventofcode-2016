import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy
from itertools import chain


class Solution:
    def solve(self, data, word, modified=False, old_states=None):
        re_swap_position = re.compile('swap position (\d+) with position (\d+)')
        re_swap_letter = re.compile('swap letter (\w+) with letter (\w+)')
        re_rotate_steps = re.compile('rotate (left|right) (\d+) steps?')
        re_rotate_position = re.compile('rotate based on position of letter (\w+)')
        re_reverse = re.compile('reverse positions (\d+) through (\d+)')
        re_move = re.compile('move position (\d+) to position (\d+)')

        if type(data) is not list:
            data = [data]

        if modified:
            data = reversed(data)
        attr = list(word)

        states = []
        print(word, end=" -> ")
        for row in data:
            states.append(''.join(attr))
            if old_states:
                if old_states[-len(states)] != states[-1]:
                    print(states[-1])
                    print(f"should have been transformed to {old_states[-len(states)]}")
                    assert old_states[-len(states)] == states[-1]
                print(states[-1])
                print(row)
            #print(states[-1])
            # print(row)
            m = re_swap_position.match(row)
            if m:
                x, y = [int(a) for a in m.groups()]
                # print(f"-> swap position {x} with {y}")
                attr[x], attr[y] = attr[y], attr[x]
                continue
            m = re_swap_letter.match(row)
            if m:
                c, d = m.groups()
                # print(f"-> swap letter {c} with {d}")
                for i in range(len(attr)):
                    if attr[i] == c:
                        attr[i] = d
                    elif attr[i] == d:
                        attr[i] = c
                continue
            m = re_rotate_steps.match(row)
            if m:
                dir = 0 if m.group(1) == 'left' else 1
                if modified:
                    dir = 1 - dir
                steps = int(m.group(2)) % len(attr)
                # print(f"-> rotate {steps} in direction {dir}")
                if dir == 0:
                    attr = [*attr[steps:], *attr[0:steps]]
                else:
                    attr = [*attr[-steps:], *attr[0:-steps]]
                continue
            m = re_rotate_position.match(row)
            if m:
                c = m.group(1)
                # print(f"-> rotate based on {c}")
                x = attr.index(c)

                # x1234567 -> +1 +0    = +1 -> 7x123456 1->0  -> 1
                # 0x234567 -> +1 +1    = +2 -> 670x2345 3->1  -> 2
                # 01x34567 -> +1 +2    = +3 -> 56701x34 5->2  -> 3
                # 012x4567 -> +1 +3    = +4 -> 4567012x 7->3  -> 4
                # 0123x567 -> +1 +4 +1 = +6 -> 23x56701 2->4  -> 6  +8+2 >> 1
                # 01234x67 -> +1 +5 +1 = +7 -> 1234x670 4->5  -> 7  +8+2 >> 1
                # 012345x7 -> +1 +6 +1 = +8 -> 012345x7 6->6  -> 8  +8+2 >> 1
                # 0123456x -> +1 +7 +1 = +9 -> x0123456 0->7  -> 9  +8+2 >> 1

                if modified:
                    if x & 1 == 1:
                        steps = (x + 1) >> 1
                    elif x == 0:
                        steps = 1
                    elif x == 4:
                        steps = 7
                    else:
                        steps = (x+10) >> 1
                    steps = steps % len(attr)

                    if steps != 0:
                        attr = [*attr[steps:], *attr[0:steps]]
                else:
                    steps = (x + 1 + (1 if x >= 4 else 0)) % len(attr)
                    attr = [*attr[-steps:], *attr[0:-steps]]
                continue
            m = re_reverse.match(row)
            if m:
                x, y = int(m.group(1)), int(m.group(2))
                # print(f"-> reverse from {x} to {y} (incl)")
                attr = [*attr[:x], *reversed(attr[x:y + 1]), *attr[y + 1:]]
                continue
            m = re_move.match(row)
            if m:
                x, y = int(m.group(1)), int(m.group(2))
                if modified:
                    x, y = y, x
                # print(f"-> move {x} to {y}")
                c = attr.pop(x)
                attr.insert(y, c)
                continue
        states.append(''.join(attr))
        print(states[-1])
        return states


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #      print(s.solve(f.read().strip().splitlines(), 'abcde'))

    with open(f'{script}.txt') as f:
        states = s.solve(f.read().strip().splitlines(), 'abcdefgh')
    #
    # print(states)
    # print('------')
    #
    # with open(f'{script}.txt') as f:
    #     print(s.solve(f.read().strip().splitlines(), 'bfheacgd', True, states))

    #with open(f'{script}-dev.txt') as f:
    #    print(s.solve(f.read().strip().splitlines(), 'decab', True))

    with open(f'{script}.txt') as f:
        s.solve(f.read().strip().splitlines(), 'fbgdceah', True)
