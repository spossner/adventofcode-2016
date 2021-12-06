import hashlib
import os
import re
import sys
from collections import deque, defaultdict
from copy import deepcopy


class Node:
    def __init__(self, id):
        self.id = id
        self.value = 1  # init of 1
        self.next = None

    def __hash__(self):
        return self.id

    def set_next(self, node):
        self.next = node

    def cut_next(self):
        assert self.next.id != self.id
        self.value += self.next.value
        self.next = self.next.next

    def __ne__(self, other):
        return self.id != other.id

    def __str__(self):
        return f"{self.id}: {self.value} -> {self.next.id if self.next is not None else 'None'}"


class Solution:
    def solve(self, n, modified=False):
        root = Node(1)
        node = root
        p = node
        p_prev = None
        for i in range(2, n+1):
            new_node = Node(i)
            node.set_next(new_node)
            node = new_node
            if i > 2 and (i % 2) == 0:
                p_prev = p
                p = p.next
        node.set_next(root)  # close circle
        node = node.next
        p = p.next if p is not None else node
        p_prev = p_prev.next if p_prev is not None else node
        while node != node.next:
            if modified:
                node.value += p.value
                p = p.next
                p_prev.next = p
                if n % 2 == 1: # do a rotation of p
                    p = p.next
                    p_prev = p_prev.next
                node = node.next
            else:
                node.cut_next()
                node = node.next
            n -= 1


        return node


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    print(s.solve(5, True))
    print(s.solve(3018458, True))
