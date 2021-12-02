from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        chars = [defaultdict(int) for i in range(len(data[0]))]
        result = []

        for row in data:
            for i, c in enumerate(row):
                chars[i][c] += 1

        for letter_count in chars:
            # print(letter_count)
            c = None
            for k, v in letter_count.items():
                #print(k, v)
                if c is None or (modified and v < c[0]) or (not modified and v > c[0]):
                    c = (v, k)
            result.append(c[1])

        return ''.join(result)


if __name__ == '__main__':
    s = Solution()
    with open('06-dev.txt') as f:
        assert s.solve(f.read().strip().splitlines()) == 'easter'

    with open('06.txt') as f:
        print(s.solve(f.read().strip().splitlines()))

    with open('06-dev.txt') as f:
        assert s.solve(f.read().strip().splitlines(), True) == 'advent'

    with open('06.txt') as f:
        print(s.solve(f.read().strip().splitlines(), True))
