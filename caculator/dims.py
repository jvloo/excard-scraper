import itertools

minHeight = 10
maxHeight = 300

minWidth = 25
maxWidth = 420

H = list(range(minHeight, maxHeight, 1))
W = list(range(minWidth, maxWidth, 1))
dimensions = list(itertools.product(*[H, W]))

def removeDuplicates(ls):
    return list({*map(tuple, map(sorted, ls))})

print(len(removeDuplicates(dimensions)))
