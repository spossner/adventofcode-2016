import os
import sys


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        count = 0

        for row in data:
            in_brace = False
            valid = False
            for i, c in enumerate(row):
                if c == '[':
                    assert in_brace is False
                    in_brace = True
                elif c == ']':
                    assert in_brace is True
                    in_brace = False
                elif i > 2 and row[i] == row[i - 3] and row[i - 1] == row[i - 2] and row[i] != row[i - 1]:
                    if in_brace:
                        valid = False
                        break # early stop because invalid word - found ABBA in braces
                    valid = True
            if valid:
                count += 1

        return count


    def solve2(self, data):
        if type(data) is not list:
            data = [data]
        count = 0

        for row in data:
            in_brace = False
            abas = set()
            babs = set()
            for i, c in enumerate(row):
                if c == '[':
                    assert in_brace is False
                    in_brace = True
                    continue
                elif c == ']':
                    assert in_brace is True
                    in_brace = False
                    continue

                if i > 1 and row[i] == row[i - 2] and row[i] != row[i - 1]: # found aba
                    aba = row[i - 2:i + 1]
                    if '[' in aba or ']' in aba:
                        continue
                    if in_brace:
                        bab = f"{aba[1]}{aba[0]}{aba[1]}"
                        # print(f"found {bab}")
                        babs.add(bab)
                    else:
                        # print(f"add {aba}")
                        abas.add(aba)

            if len(abas.intersection(babs)) > 0:
                # print(row)
                count += 1

        return count


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    s = Solution()

    # assert s.solve('abba[mnop]qrst') == 1
    # assert s.solve('ioxxoj[asdfgh]zxcvbn') == 1
    # assert s.solve('abcd[bddb]xyyx') == 0
    # assert s.solve('aaaa[qwer]tyui') == 0

    # with open(f'{script}.txt') as f:
    #    print(s.solve(f.read().strip().splitlines()))

    assert s.solve2('aba[bab]xyz') == 1
    assert s.solve2('aaa[kek]eke') == 1
    assert s.solve2('xyx[xyx]xyx') == 0
    assert s.solve2('zazbz[bzb]cdb') == 1
    with open(f'{script}.txt') as f:
        print(s.solve2(f.read().strip().splitlines()))