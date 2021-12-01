import re
import itertools


class Solution:
    def solve(self, data):
        if type(data) is not list:
            data = [data]
        valid = 0
        for row in data:
            a, b, c = [int(x) for x in row.split()]
            if a + b > c and a + c > b and b + c > a:
                valid = valid + 1
        return valid

    def solve2(self, data):
        if type(data) is not list:
            data = [data]
        data = [row.split() for row in data]
        valid = 0
        for y in range(0, len(data), 3):
            print(f"all triangles starting at row {y}")
            for x in range(3):
                print(f"triangles in column {x}")
                a = int(data[y][x])
                b = int(data[y+1][x])
                c = int(data[y+2][x])
                print(a,b,c)
                if a + b > c and a + c > b and b + c > a:
                    valid = valid + 1
        return valid



if __name__ == '__main__':
    s = Solution()
    # print(s.solve("5 10 25"))

    #with open('03.txt') as f:
    #    print(s.solve(f.read().strip().splitlines()))

    with open('03.txt') as f:
        print(s.solve2(f.read().strip().splitlines()))
