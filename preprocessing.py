# preprocessing.py
# Loads and pre-processes Shakespearean sonnet data to train on.

def processed_shakespeare_data():
    '''
    Takes in the data in the form outputted by `load_shakespeare` or
    `load_spenser` and processes it to generate a list of sequences for each
    sonnet. Returns `data`, the sequences as a list of lists of integers, as
    well as `dictionary`, which maps each integer to a word.
    For now, we ignore punctuation and treat the entire sonnet as a single
    training sequence.
    '''
    sonnets = load_shakespeare()

    # Tokenize the sonnets into individual words.
    X = []
    for sonnet in sonnets:
        line_new = []
        for line in sonnet:
            for word in line.split():
                if word[0] == '(':
                    word = word[1:]
                if word[0] == "'" and word[1:].lower() not in \
                ['gainst', 'greeing,', 'scaped', 'tis', 'twixt']:
                    word = word[1:]
                if word[-1] in [',', '.', '?', '!', ':', ';', ')']:
                    word = word[:-1]
                if word[-1] == "'" and word[:-1].lower() not in ['t', 'th']:
                    word = word[:-1]
                if word[-1] in [',', '.', '?', '!', ':', ';', ')']:
                    word = word[:-1]
                line_new.append(word.lower())
        X.append(line_new)

    # Convert the sequences of words to sequences of integers.
    syllable_dict = load_syllable_dict()
    dictionary = [word[0] for word in syllable_dict]
    for i in range(len(X)):         # loop over each sonnet
        for j in range(len(X[i])):  # loop over every word in each sonnet
            X[i][j] = dictionary.index(X[i][j])

    # Create dictionaries for syllable information.
    syllables = {}
    end_syllables = {}
    for word in syllable_dict:
        syllables[word[0]] = word[2]
        end_syllables[word[0]] = word[1]

    return X, dictionary, syllables, end_syllables

def load_shakespeare():
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

def load_spenser():
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

def load_syllable_dict():
    '''
    Loads the syllable dictionary from the text file and returns it as a list of
    lists. Each element in the list has this form:
        [word, end, syllables]
            word:       the word
            end:        the number of syllables in the word if it appears at the
                        end of the line. (if `end` is 0, then the word does not
                        appear at the end of a line.)
            syllables:  a list of integers, representing the possible number of
                        syllables the word can have
    '''
    words = []
    f = open('data/syllable_dictionary.txt', 'r')
    for line in f:
        line = line.split()
        word = []
        word.append(line[0])
        end = 0
        syllables = []
        for i in range(1, len(line)):
            if line[i][0] == 'E':
                end = int(line[i][1:])
            else:
                syllables.append(int(line[i]))
        word.append(end)
        word.append(syllables)
        words.append(word)
    f.close()
    return words
