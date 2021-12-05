import re
from itertools import chain, combinations
from collections import defaultdict, deque, Counter

class Solution:
    def solve(self, data, modified=False):
        ptr = 0
        registers = defaultdict(int)
        if modified:
            registers['c'] = 1
        while ptr < len(data):
            instr = data[ptr].split(' ')
            cmd = instr[0]
            if cmd == 'inc':
                registers[instr[1]] += 1
            elif cmd == 'dec':
                registers[instr[1]] -= 1
            elif cmd == 'cpy':
                registers[instr[2]] = int(instr[1]) if instr[1].isnumeric() else registers[instr[1]]
            elif cmd == 'jnz':
                if (instr[1].isnumeric() and int(instr[1]) != 0) or (not instr[1].isnumeric() and registers[instr[1]] != 0):
                    ptr += int(instr[2])
                    continue # ptr set to new value
            else:
                raise SyntaxError(f'unexpected command {data[ptr]} at line {ptr}')
            ptr += 1
        return registers
    
            
if __name__ == '__main__':
    s = Solution()
    with open('12.txt') as f:
        print(s.solve(f.read().strip().splitlines(), True))

