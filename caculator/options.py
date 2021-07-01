import itertools

# catOptions = ['Custom Die-Cut', 'Rectangle/Square', 'Round', 'Standard Shape', 'Multiple Dieline']
#
# cutOptions = ['Cut To Size', 'Die-Cutting']
#
# paperOptions = ['Mirror Kote', 'Printing Paper', 'Transparent OPP', 'Removable Transparent OPP',
#     'Synthetic Paper', 'White PP (Polypropylene)', 'Bright Silver Polyester',
#     'Matte Silver Polyester', 'Removable White PP', 'Brown Craft Paper']
#
# finishOptions = ['Not Required', 'Matte Laminate (Front)', 'Gloss Laminate (Front)',
#     'Gloss Water Based Varnish', 'UV Varnish', 'Soft Touch Laminate (Front)']

catOptions = ['Custom Die-Cut', 'Rectangle/Square', 'Round', 'Standard Shape']

# cutOptions = ['Cut To Size', 'Die-Cutting']

paperOptions = ['Mirror Kote', 'Printing Paper', 'Transparent OPP', 'Synthetic Paper', 'White PP (Polypropylene)']

finishOptions = ['Not Required', 'Matte Laminate (Front)', 'Gloss Laminate (Front)', 'UV Varnish']

# options = [catOptions, cutOptions, paperOptions, finishOptions]
options = [catOptions, paperOptions, finishOptions]

options = list(itertools.product(*options))

print(len(options))
