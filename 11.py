import re
from itertools import chain, combinations
from collections import deque, Counter

class Solution:
    def __init__(self, data) -> None:
        self.floors = [set(re.findall(r'(\w+)(?:-compatible)? (microchip|generator)', line)) for line in data]
        # PART II
        self.floors[0] = self.floors[0].union([('elerium', 'generator'), ('elerium', 'microchip'),
                                 ('dilithium', 'generator'), ('dilithium', 'microchip')])
        print(self.floors)

    def is_valid_transition(self, floor):
        return len(set(type for _, type in floor)) < 2 or \
            all((obj, 'generator') in floor
                for (obj, type) in floor
                if type == 'microchip')

    def next_states(self, state):
        moves, elevator, floors = state

        possible_moves = chain(combinations(floors[elevator], 2), combinations(floors[elevator], 1))

        for move in possible_moves:
            for direction in [-1, 1]:
                next_elevator = elevator + direction
                if not 0 <= next_elevator < len(floors):
                    continue

                next_floors = floors.copy()
                next_floors[elevator] = next_floors[elevator].difference(move)
                next_floors[next_elevator] = next_floors[next_elevator].union(move)

                if (self.is_valid_transition(next_floors[elevator]) and self.is_valid_transition(next_floors[next_elevator])):
                    yield (moves + 1, next_elevator, next_floors)
    
    def is_all_top_level(self, floors):
        return all(not floor
            for number, floor in enumerate(floors)
            if number < len(floors) - 1)

    def count_floor_objects(self, state):
        _, elevator, floors = state
        return elevator, tuple(tuple(Counter(type for _, type in floor).most_common()) for floor in floors)

    def solve(self):
        seen = set()
        queue = deque([(0, 0, self.floors)])

        while queue:
            state = queue.popleft()
            moves, _, floors = state
            print(moves, floors)

            if self.is_all_top_level(floors):
                return moves

            for next_state in self.next_states(state):
                if (key := self.count_floor_objects(next_state)) not in seen:
                    seen.add(key)
                    queue.append(next_state)


if __name__ == '__main__':
    
    with open('11.txt') as f:
        s = Solution(f.read().strip().splitlines())
        print(s.solve())

