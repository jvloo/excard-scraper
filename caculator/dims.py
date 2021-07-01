import itertools

minHeight = 10
maxHeight = 300

minWidth = 25
maxWidth = 420

H = list(range(minHeight, maxHeight, 10))
W = list(range(minWidth, maxWidth, 10))
dimensions = list(itertools.product(*[H, W]))

print(len(dimensions))
