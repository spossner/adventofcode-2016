import re
import itertools
from collections import defaultdict


class Solution:
    def solve(self, data):
        if type(data) is not list:
            data = [data]

        total = 0

        for row in data:
            parts = row.split('-')
            id, checksum = parts[-1].split('[')
            id = int(id)
            checksum = checksum[:-1]
            parts = parts[:-1]

            letters = ''.join(parts)
            chars = defaultdict(int)
            for c in letters:
                chars[c] += 1
            sorted_chars = defaultdict(list)
            for k, v in chars.items():
                sorted_chars[v].append(k)
            check = ''
            for k in sorted(sorted_chars, reverse=True):
                v = sorted_chars[k]
                check = f"{check}{''.join(sorted(v))}"
            if check[:5] == checksum:
                for p in parts:
                    for c in p:
                        print(chr((((ord(c) - 97) + id) % 26) + 97), end='')
                    print(' ', end='')
                print(f" -> {id}")

        return total


if __name__ == '__main__':
    s = Solution()
    with open('04-dev.txt') as f:
        print(s.solve(f.read().strip().splitlines()))

    with open('04.txt') as f:
        print(s.solve(f.read().strip().splitlines()))
