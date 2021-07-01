import itertools

minHeight = 10
maxHeight = 300

minWidth = 25
maxWidth = 420

H = list(range(minHeight, maxHeight, 1))
W = list(range(minWidth, maxWidth, 1))
dimensions = list(itertools.product(*[H, W]))

def removeDuplicates(ls):
    return sorted(sorted(list({*map(tuple, map(sorted, ls))}), key=lambda x: x[0]), key=lambda x: x[1])

print(len(removeDuplicates(dimensions)))
