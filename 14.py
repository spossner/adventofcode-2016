import hashlib
import os
import sys
from collections import deque, defaultdict


class Solution:
    def triplet_char(self, s):
        for i in range(2,len(s)):
            if s[i] == s[i-1] and s[i] == s[i-2]:
                return s[i]
        return None


    def solve(self, salt, modified=False):
        candidates = deque()
        results = []
        i = 0
        while len(results) < 64:
            t = hashlib.md5(f"{salt}{i}".encode()).hexdigest()
            if modified:
                for _ in range(2016):
                    t = hashlib.md5(t.encode()).hexdigest()
            tc = self.triplet_char(t)

            if candidates:
                while candidates[0][2] is not None or candidates[0][0] <= i-1000:
                    c = candidates.popleft()
                    if c[2] is not None:
                        results.append(c)

                for c in candidates:
                    if c[1] in t:
                        print(f"match {c} because of {i}: {t}")
                        c[2] = i

            if tc:
                candidates.append([i, tc * 5, None, t]) # (i, 5x triplet-char, match-i, hash)

            i = i + 1

        return results[63][0]


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    s = Solution()
    #print(s.solve('abc', True))
    print(s.solve('jlmsuwbz', True))