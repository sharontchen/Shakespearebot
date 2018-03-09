# preprocessing.py
# Loads and pre-processes Shakespearean sonnet data to train on.

def processed_shakespeare_data():
    '''
    Process dataset of all Shakespearean sonnets. We ignore punctuation and
    treat each sonnet as a single training sequence.

    Outputs:
        X               The input sequences. Each sequence is a sonnet, and each
                        sonnet is represented as a list of integers, where the
                        integer is the index of the word in `dictionary`.
        dictionary      A list of all the words in all of Shakespeare's sonnets.
        syllables       A Python dictionary which maps a word to a list of the
                        number of syllables that word can have.
        end_syllables   A Python dictionary which maps a word to a number
                        representing the number of syllables it has when the
                        word appears at the end of the line. If the number is 0,
                        then the word doesn't appear at the end of a line.
    '''
    sonnets = load_shakespeare()

    # Tokenize the sonnets into individual words.
    X = []
    for i, sonnet in enumerate(sonnets):
        if i != 98 and i != 125:    # ignore sonnets 99 and 126
            sonnet_new = []
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
                    sonnet_new.append(word.lower())
            X.append(sonnet_new)

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

def processed_shakespeare_data2():
    '''
    Process dataset of all Shakespearean sonnets. We ignore punctuation and
    treat each line as a single training sequence.

    Outputs:
        X               The input sequences. Each sequence is a line, and each
                        line is represented as a list of integers, where the
                        integer is the index of the word in `dictionary`.
        dictionary      A list of all the words in all of Shakespeare's sonnets.
        syllables       A Python dictionary which maps a word to a list of the
                        number of syllables that word can have.
        end_syllables   A Python dictionary which maps a word to a number
                        representing the number of syllables it has when the
                        word appears at the end of the line. If the number is 0,
                        then the word doesn't appear at the end of a line.
        rhyme_dict      A list of lists of the form [word1, word2], where word1
                        and word2 are rhyming words. The words are represented
                        as integers corresponding to the index of the word in
                        `dictionary`.
    '''
    # Load dictionary from text file.
    syllable_dict = load_syllable_dict()
    dictionary = [word[0] for word in syllable_dict]

    # Create dictionaries for syllable information.
    syllables = {}
    end_syllables = {}
    for word in syllable_dict:
        syllables[word[0]] = word[2]
        end_syllables[word[0]] = word[1]

    # Load Shakespeare's sonnets.
    sonnets = load_shakespeare()

    # Tokenize the sonnets into individual words, represented as integers.
    data = []
    for i, sonnet in enumerate(sonnets):
        sonnet_new = []
        for line in sonnet:
            line_new = []
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
                line_new.append(dictionary.index(word.lower()))
            sonnet_new.append(line_new)
        data.append(sonnet_new)

    # Generate rhyming dictionary based on the words that appear at the end of
    # the lines in Shakspeare's sonnets.
    rhyme_dict = []
    for i, sonnet in enumerate(data):  # rhyme scheme is abab cdcd efef gg
        if i != 98 and i != 125:    # ignore sonnets 99 and 126
            rhyme_dict.append([sonnet[0][-1], sonnet[2][-1]])
            rhyme_dict.append([sonnet[1][-1], sonnet[3][-1]])
            rhyme_dict.append([sonnet[4][-1], sonnet[6][-1]])
            rhyme_dict.append([sonnet[5][-1], sonnet[7][-1]])
            rhyme_dict.append([sonnet[8][-1], sonnet[10][-1]])
            rhyme_dict.append([sonnet[9][-1], sonnet[11][-1]])
            rhyme_dict.append([sonnet[12][-1], sonnet[13][-1]])

    # Right now, `X` is a list of list of lists. The outer list contains each
    # sonnet, the middle list contains each line in the sonnet, and the inner
    # list contains each word in the line.
    # Convert `X` to a list of lists, so it becomes a list of input sequences we
    # can train on. Do this by just ignoring the sonnet and treating every line
    # as the same.
    X = [x for y in data for x in y]

    return X, dictionary, syllables, end_syllables, rhyme_dict

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
