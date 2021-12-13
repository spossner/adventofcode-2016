from collections import deque
from itertools import permutations


# find positions of characters in the map that are accepted by the predicate
def find_in_map(mp, predicate):
    return [(i, j) for i in range(len(mp)) for j in range(len(mp[i])) if predicate(mp[i][j])]


# bfs distance from (y_fr,x_fr) to (y_to,x_to) assuming walls all around
moves = set([(-1, 0), (1, 0), (0, 1), (0, -1)])


def bfs_from_to(mp, fr, to):
    q = deque([(0, fr)])
    vis = set([fr])
    while q:
        dst, cur = q.pop()
        if cur == to:
            return dst
        y, x = cur
        for dy, dx in moves:
            ny, nx = y + dy, x + dx
            if mp[ny][nx] != '#' and (ny, nx) not in vis:
                q.appendleft((dst + 1, (ny, nx)))
                vis.add((ny, nx))
    return -1


def solve(inp):
    zero_pos = find_in_map(inp, lambda x: x == '0')[0]
    # find all non-zero positions
    nums_pos = find_in_map(inp, lambda x: x in map(str, range(1, 10)))
    # precompute distance from 0 to all other numbers
    dst_0 = [bfs_from_to(inp, zero_pos, n_pos) for n_pos in nums_pos]
    K = len(nums_pos)
    # precompute all pairwise K^2 / 2 distances
    dsts = [[None for j in range(K)] for i in range(K)]
    for i in range(K):
        for j in range(i + 1, K):
            dsts[j][i] = dsts[i][j] = bfs_from_to(inp, nums_pos[i], nums_pos[j])
    part1, part2 = 1e12, 1e12
    # with all pairwise distances computed the problem is reduced to TSP
    # O(K!) is terrible but good enough for K=7 :)
    for path in permutations(range(K)):
        dst = dst_0[path[0]]
        for i in range(len(path) - 1):
            dst += dsts[path[i]][path[i + 1]]
        part1 = min(part1, dst)
        dst += dst_0[path[-1]]
        part2 = min(part2, dst)
    return part1, part2


inp = [line.strip() for line in open('24.txt').readlines()]
print(solve(inp))
