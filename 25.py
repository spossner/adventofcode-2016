import os
import random
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        ops = [cmd.split(' ') for cmd in data]
        i = 0
        while True:
            print(f"\n{i}", end=": ")
            registers = defaultdict(int)
            registers['a'] = i
            ptr = 0
            count = 0
            next_signal = 0
            while ptr < len(ops):
                instr = ops[ptr]
                cmd = instr[0]
                if count > 300:
                    print("\nSEEMS TO BE GOOD")
                    return i
                if cmd == 'nop':
                    pass
                elif cmd == 'out':
                    try:
                        signal = int(instr[1])
                    except ValueError:
                        signal = registers[instr[1]]
                    print(str(signal), end=', ')
                    count += 1
                    if signal != next_signal:
                        break
                    next_signal = 1 - next_signal
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
            i += 1

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    # with open(f'{script}-dev.txt') as f:
    #     print(s.solve(f.read().strip().splitlines()))

    with open(f'{script}.txt') as f:
        print(s.solve(f.read().strip().splitlines()))
