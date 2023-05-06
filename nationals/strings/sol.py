from itertools import product

# Random base flag
s = list("DDC{GhostintheShell_vs_lleHSyniT!_Kalmar_or_DDC_best_at_strings??}")

# strings strings | grep DDC{G > fakeflags.txt
with open("fakeflags.txt") as f:
    fakeflags = set(f.read().strip().split("\n"))

idxs = [6, 9, 13, 16, 25, 30, 32, 35, 38, 41, 49, 53, 59, 63, 64]
options = ['o0', 'i1', 'e3', 'e3', 'e3', 'i1', '!?', 'a4', 'a4', 'o0', 'e3', 'a4', 'i1', '!?', '!?']

flags = set()
for option in product(*options):
    for i, c in zip(idxs, option):
        s[i] = c
    flags.add("".join(s))

remaining = flags - fakeflags

assert len(remaining) == 1

flag = remaining.pop()
print(flag)