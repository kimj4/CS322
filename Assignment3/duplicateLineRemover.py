s = set()

numlines = 0
with open('cfg_alternate', 'r') as f:
    for line in f:
        if len(line) > 1:
            s.add(line)
            numlines += 1

nonterminals = set()

for a in s:
    # store nonterminals
    nonterminals.add(a.strip().split(' ')[0])
    print(a.strip().split(' '))

print(nonterminals)

terminalRules = {}
nonTerminalRules = []

for a in s:
    if ( (len(a.strip().split(' ')) == 3) and (a.strip().split(' ')[-1] not in nonterminals) ):
        if a.strip().split(' ')[0] in terminalRules:
            terminalRules[a.strip().split(' ')[0]] += ' | \'' + a.strip().split(' ')[-1] + '\''
        else:
            terminalRules[a.strip().split(' ')[0]] = '\'' + a.strip() + '\''
    else:
        nonTerminalRules.append(a.strip())

for key, value in terminalRules.items():
    print(value)

with open('reducedCFG.txt', 'w') as f:
    for a in nonTerminalRules:
        f.write(a + '\n')

with open('reducedCFG.txt', 'a') as f:
    for a, b in terminalRules.items():
        f.write(b + '\n')


# l = sorted(list(s))
# with open('reducedCFG.txt', 'w') as f:
#     for a in l:
#         f.write(a)
