import os
import sys


class Solution:
    def solve(self, data):
        in_marker = False
        marker = ''
        result = 0
        pattern = ''
        l = 0   # pattern length after marker
        rep = 0 # repeat count
        for c in data:
            if in_marker:
                if l > 0:
                    # build pattern
                    pattern = pattern + c
                    l = l - 1
                    if l == 0:
                        # got pattern
                        result += (rep * s.solve(pattern))
                        pattern = ''
                        rep = 0
                        in_marker = False
                elif c == ')':
                    l, rep = [int(a) for a in marker.split('x')]
                    marker = ''
                else:
                    marker = marker + c
            else:
                if c == '(':
                    in_marker = True
                else:
                    result += 1
        return result


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    assert s.solve('(3x3)XYZ') == 9
    assert s.solve('X(8x2)(3x3)ABCY') == 20
    assert s.solve('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
    assert s.solve('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip()))
