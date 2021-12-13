import hashlib
import os
import queue
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy
from functools import reduce, total_ordering
from itertools import chain

WIDTH = 32
HEIGHT = 31


# WIDTH = 3
# HEIGHT = 3


@total_ordering
class Node:
    def __init__(self, x, y, size, used, avail, payload=False):
        self.id = y * WIDTH + x
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.payload = payload

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_neighbour(self, other):
        return self.distance(other) == 1

    def set_payload(self):
        self.payload = True

    def clean(self):
        u = self.used
        self.avail += u
        self.used = 0
        pl = self.payload
        self.payload = False
        return (u, pl)

    def load(self, l):
        self.used += l
        self.avail -= l

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return self.id

    def __str__(self):
        return f"<{self.x},{self.y}: {self.size}T, used {self.used}T, avail {self.avail}T>"

    def __repr__(self):
        return self.__str__()


class Solution:
    def adjacent_nodes(self, id):
        y = int(id / WIDTH)
        x = id % WIDTH
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if nx < 0 or ny < 0 or nx >= WIDTH or ny >= HEIGHT:
                continue
            yield ny * WIDTH + nx

    def is_neighbour(self, p1, p2):
        return p1[0] == p2[0] and abs(p1[1] - p2[1]) == 1 or p1[1] == p2[1] and abs(p1[0] - p2[0]) == 1

    def manhatten_distance(self, paylod_id):
        return (paylod_id % WIDTH) + int(paylod_id / WIDTH)

    def solve(self, data, modified=False):
        self.nodes = {int(y) * WIDTH + int(x): Node(int(x), int(y), int(s), int(u), int(a)) for (x, y, s, u, a, p) in
                      re.findall('/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%', data)}

        print(self.nodes)
        result = set()

        for a in self.nodes.values():
            for b in self.nodes.values():
                if a == b or a.used == 0 or a.used > b.avail:
                    continue
                result.add((min(a.id, b.id), max(a.id, b.id)))
        print(result)
        return len(result)

    def solve2(self, data, modified=False):
        nodes = re.findall('/dev/grid/node-x(\d+)-y(\d+)\s+\d+T\s+(\d+)T\s+(\d+)T\s+\d+%', data)
        init_state = [None] * (WIDTH * HEIGHT)
        for (x, y, u, a) in nodes:
            id = int(y) * WIDTH + int(x)
            init_state[id] = (int(u), int(a))  # used, avail
        print(init_state)

        candidates = deque()
        for i, n in enumerate(init_state):
            candidates.append((i, WIDTH - 1, WIDTH - 1, 0, deepcopy(init_state)))  # node-id, payload-id, distance, #moves, state

        seen = set()
        while candidates:
            print('.')
            for _ in range(len(candidates)):
                id, payload_id, distance, moves, state = candidates.popleft()
                if payload_id == 0:
                    return moves
                if state[id][0] == 0:  # used == 0 -> empty node -> ignore
                    continue
                key = (id, payload_id, tuple(state))
                if key in seen:
                    continue
                seen.add(key)
                for adj in self.adjacent_nodes(id):
                    if state[adj][1] < state[id][0]:
                        continue
                    if id == payload_id:
                        payload_id = adj  # moved relevant payload to adj
                        d = self.manhatten_distance(payload_id)
                        if d > distance:  # ignore bad solutions
                            continue
                        distance = d

                    print(f"{id} -> {adj}")
                    new_state = list(deepcopy(state))
                    data = new_state[id][0]
                    new_state[id] = (0, new_state[id][1] + data)
                    new_state[adj] = (new_state[adj][0] + data, new_state[adj][1] - data)

                    for c in self.adjacent_nodes(id):
                        candidates.append((c, payload_id, distance, moves + 1, new_state))  # node-id, payload-id, distance, #moves, state

    def solve3(self, data):
        if type(data) is not list:
            data = [data]

        sizes = {}
        usage = {}

        for line in data:
            if not line.startswith('/dev/grid/'):
                continue

            name, size, used, available, percent = line.strip().split()
            _, xs, ys = name.split('/')[-1].split('-')
            x = int(xs[1:])
            y = int(ys[1:])

            sizes[x, y] = int(size[:-1])
            usage[x, y] = int(used[:-1])

        goal = (WIDTH - 1, 0)
        self.print_usage_icons(sizes, usage, goal)

        # Find the empty node
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if usage[x, y] == 0:
                    (empty_x, empty_y) = empty = (x, y)

        # Find walls (nodes with more than 500T data)
        walls = {
            (x, y)
            for x in range(WIDTH)
            for y in range(HEIGHT)
            if sizes[x, y] > 500
        }

        # Use dynamic programming to find the minimum distance between two points
        distance_from_empty = {}
        to_calculate = deque()

        to_calculate.append((empty, 0))
        while to_calculate:
            point, distance = to_calculate.popleft()
            if point in distance_from_empty:
                continue

            distance_from_empty[point] = distance

            (x, y) = point
            for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + xd, y + yd)
                if 0 <= x + xd < WIDTH and 0 <= y + yd < HEIGHT and neighbor not in walls:
                    to_calculate.append((neighbor, distance + 1))

        # Move to immediately beside the goal
        distance_to_goal = distance_from_empty[(WIDTH - 2, 0)]

        # Now it takes 5 to move the goal one left and reset (except the last time)
        distance_to_zero = 5 * (WIDTH - 2) + 1

        print('Best guess = {} ({} to goal + {} to zero)'.format(
            distance_to_goal + distance_to_zero,
            distance_to_goal,
            distance_to_zero,
        ))

    def print_usage_icons(self, sizes, usage, goal):
        '''Print based on the hint in the puzzle.'''

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == goal:
                    output = 'G'
                elif usage[x, y] == 0:
                    output = '@'
                elif sizes[x, y] > 500:
                    output = '#'
                else:
                    output = '.'

                print(output, end='')
            print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #      print(s.solve3(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
        print(s.solve3(f.read().strip().splitlines()))
