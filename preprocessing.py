# preprocessing.py
# Loads and pre-processes Shakespearean sonnet data to train on.
from Poetry_Tools import poetrytools

def processed_shakespeare_data():
    '''
    Process dataset of all Shakespearean sonnets. We ignore punctuation and
    treat each sonnet as a single training sequence.

    Outputs:
        X               The input sequences. Each sequence is a sonnet, and each
                        sonnet is represented as a list of integers, where the
                        integer is the index of the word in `dictionary`.
        dictionary      A list of all the words in all of Shakespeare's sonnets.
        syllables       A list which stores the possible number of syllables a
                        word can have. Each element of `syllables` is a list.
                        The indices of the words are the same as the indices of
                        `dictionary`.
        end_syllables   A list of the number of syllables each word has when it
                        appears at the end of the line. If the number is 0, then
                        the word doesn't appear at the end of a line.
    '''
    sonnets = load_shakespeare()

    # Tokenize the sonnets into individual words.
    X = []
    for i, sonnet in enumerate(sonnets):
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

    # Capitalize 'i' in the dictionary.
    dictionary[1365] = dictionary[1365].upper()

    # Create lists for syllable information.
    syllables = []
    end_syllables = []
    for word in syllable_dict:
        syllables.append(word[2])
        end_syllables.append(word[1])

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
        syllables       A list which stores the possible number of syllables a
                        word can have. Each element of `syllables` is a list.
                        The indices of the words are the same as the indices of
                        `dictionary`.
        end_syllables   A list which stores the possible number of syllables a
                        word can have if it appears at the end of a line. Each
                        element of `end_syllables` is a list. The indices of the
                        words are the same as the indices of `dictionary`.
        rhyme_dict      A list of lists of the form [word1, word2], where word1
                        and word2 are rhyming words. The words are represented
                        as integers corresponding to the index of the word in
                        `dictionary`.
        stress_dict:    List of lists of integers; each list in stress_dict has
                        two elements, where first and second element is whether
                        the word starts/ends with stressed syllable.
    '''
    # Load dictionary from text file.
    syllable_dict = load_syllable_dict()
    dictionary = [word[0] for word in syllable_dict]

    # Create lists for syllable information.
    syllables = []
    end_syllables = []
    for word in syllable_dict:
        syllables.append(word[2])
        end_syllables.append(word[1])

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

    dictionary[1365] = dictionary[1365].upper()  # capitalize 'i'
    dictionary[1366] = dictionary[1366].capitalize()  # capitalize "i'll"

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

    stress_dict = process_stress_dict(dictionary)
    return X, dictionary, syllables, end_syllables, rhyme_dict, stress_dict

def process_stress_dict(dictionary):
    '''
    Returns stress dictionary a list of lists indexed in the same way as dictionary in
    processed_shakespeare_data.

    dictionary:     A list of all the words in all of Shakespeare's sonnets.
    stress_dict:    List of lists of integers; each list in stress_dict has two
                    elements, where first and second element is whether the
                    word starts/ends with stressed syllable.
    '''
    stress_dict_helper = poetrytools.scanscion([dictionary])[0]
    stress_dict = []
    for stresses in stress_dict_helper:
        stress = []
        if stresses[0] == '1':
            stress.append(1)
        else:
            stress.append(0)
        if stresses[-1] == '1':
            stress.append(1)
        else:
            stress.append(0)
        stress_dict.append(stress)
    return stress_dict

def punctuation_freq_shakespeare():
    '''
    Returns two lists of the frequencies with which six punctuation marks appear
    in Shakespeare's sonnets.

    punct_marks     a list of punctuation marks [',', '.', ':', '!', ';', '?']
    punct_freq      a list of the frequencies with which each of the six
                    punctuation marks appear. normalized to sum to 1.
    '''
    punct_marks = [',', '.', ':', '!', ';', '?']
    punct_freq = [0, 0, 0, 0, 0, 0]
    with open('data/shakespeare.txt') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            if c in punct_marks:
                punct_freq[punct_marks.index(c)] += 1
    punct_sum = sum(punct_freq)
    punct_freq = [x / punct_sum for x in punct_freq]
    return punct_marks, punct_freq

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
            end:        a list of integers, representing the possible number of
                        syllables the word can have if it appears at the end of
                        the line
            syllables:  a list of integers, representing the possible number of
                        syllables the word can have
    '''
    words = []
    f = open('data/syllable_dictionary.txt', 'r')
    for line in f:
        line = line.split()
        word = []
        word.append(line[0])
        end = []
        syllables = []
        for i in range(1, len(line)):
            if line[i][0] == 'E':
                end.append(int(line[i][1:]))
            else:
                syllables.append(int(line[i]))
        if end == []:
            end = syllables
        word.append(end)
        word.append(syllables)
        words.append(word)
    f.close()
    return words
