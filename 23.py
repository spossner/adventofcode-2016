import os
import random
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        ops = [cmd.split(' ') for cmd in data]

        ptr = 0
        count = 0
        registers = defaultdict(int)
        # if modified:
        registers['a'] = 12
        while ptr < len(ops):
            count += 1
            instr = ops[ptr]
            if ptr == 4: # quick fix multiplication in line 0x04:
                registers['a'] = registers['b'] * registers['d']
                print(f"inject mul {registers['b']} * {registers['d']} = {registers['a']}")
                registers['c'] = 0
                registers['d'] = 0
                ptr = 10 # continue at line 10
                continue
            if count % 1000000 == 0:
                print(f"{count}: {ptr} > {instr}\n{registers}")
            # print(f"{ptr:<6}: {instr}")
            cmd = instr[0]
            if cmd == 'nop':
                pass
            elif cmd == 'add':
                try:
                    registers[instr[2]] += int(instr[1])
                except ValueError:
                    registers[instr[2]] += registers[instr[1]]
            elif cmd == 'mul':
                try:
                    registers[instr[2]] = int(instr[1]) * registers[instr[2]]
                except ValueError:
                    registers[instr[2]] = registers[instr[1]] * registers[instr[2]]
            elif cmd == 'inc':
                if not instr[1].isnumeric():
                    registers[instr[1]] += 1
            elif cmd == 'dec':
                if not instr[1].isnumeric():
                    registers[instr[1]] -= 1
            elif cmd == 'cpy':
                if not instr[2].isnumeric():
                    try:
                        registers[instr[2]] = int(instr[1])
                    except ValueError:
                        registers[instr[2]] = registers[instr[1]]
            elif cmd == 'jnz':
                if (instr[1].isnumeric() and int(instr[1]) != 0) or (not instr[1].isnumeric() and registers[instr[1]] != 0):
                    try:
                        ptr += int(instr[2])
                    except ValueError:
                        ptr += registers[instr[2]]
                    continue  # ptr set to new value
            elif cmd == 'tgl':
                try:
                    p = ptr + int(instr[1])
                except ValueError:
                    p = ptr + registers[instr[1]]

                if p >= 0 and p < len(ops):
                    o = ops[p]
                    # print(f"toggle {o} to ", end='')
                    if len(o) == 2:
                        o[0] = 'dec' if o[0] == 'inc' else 'inc'
                    elif len(o) == 3:
                        o[0] = 'cpy' if o[0] == 'jnz' else 'jnz'
                    # print(o)
            else:
                raise SyntaxError(f'unexpected command {instr} at line {ptr}')
            ptr += 1
        return registers


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip().splitlines()))
