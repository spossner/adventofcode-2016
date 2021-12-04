import os
import sys


class Solution:
    def solve(self, data):
        in_marker = False
        marker = ''
        result = ''
        pattern = ''
        l = 0
        rep = 0
        for c in data:
            if in_marker:
                if l > 0:
                    # build pattern
                    pattern = pattern + c
                    l = l - 1
                    if l == 0:
                        # got pattern
                        for i in range(rep):
                            result = result + pattern
                        pattern = ''
                        rep = 0
                        in_marker = False
                elif c == ')':
                    l, rep = [int(a) for a in marker.split('x')]
                    # print(marker, l, rep)
                    marker = ''
                else:
                    marker = marker + c
            else:
                if c == '(':
                    in_marker = True
                else:
                    result = result + c
        print(result)
        return len(result)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    assert s.solve('ADVENT') == 6
    assert s.solve('A(1x5)BC') == 7
    assert s.solve('(3x3)XYZ') == 9
    assert s.solve('A(2x2)BCD(2x2)EFG') == 11
    assert s.solve('(6x1)(1x3)A') == 6
    assert s.solve('X(8x2)(3x3)ABCY') == 18

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip()))
