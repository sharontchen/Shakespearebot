# preprocessing.py
# ----------------
# Loads and pre-processes Shakespearean sonnet data to train on.

def import_shakespeare():
    '''
    Imports dataset of Shakespearean sonnets and returns all the sonnets as a
    list of lists. Each element is a sublist representing a sonnet, and each
    element of the sublist is a line of the sonnet. This function does not
    process the data (e.g. remove punctuation, tokenize words) at all; it just
    loads the dataset.
    '''
    sonnets = []
    sonnet = []
    f = open('data/shakespeare.txt', 'r')
    for line in f:
        if line.strip().isdigit():
            sonnet = []
            sonnets.append(sonnet)
        elif line.strip() != '':
            sonnet.append(line.strip())
    f.close()
    return sonnets

def import_spenser():
    '''
    Imports dataset of Spenser's sonnets and returns all the sonnets as a list
    of lists. Each element is a sublist representing a sonnet, and each element
    of the sublist is a line of the sonnet. This function does not process the
    data (e.g. remove punctuation, tokenize words) at all; it just loads the
    dataset.
    '''
    sonnets = []
    sonnet = []
    f = open('data/spenser.txt', 'r')
    for line in f:
        if line.strip() != '' and len(line.strip()) <= 10:
            sonnet = []
            sonnets.append(sonnet)
        elif line.strip() != '':
            sonnet.append(line.strip())
    f.close()
    return sonnets
