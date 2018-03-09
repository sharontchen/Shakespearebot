from HMM import unsupervised_HMM
from preprocessing import processed_shakespeare_data
from preprocessing import processed_shakespeare_data2
import random

def naive_poem_generator(n_states, N_iters, k):
    '''
    Trains an HMM using unsupervised learning and generates k 14-line sonnets.

    Arguments:
        k:          Number of sonnets to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning (EM algorithm)
    '''
    # Data to train on from pre-processing
    data, words_list, syllables, end_syllables = processed_shakespeare_data()

    # Generate k input sequences.
    for i in range(k):

        print('Training unsupervised HMM...')

        # Train the HMM.
        HMM = unsupervised_HMM(data, n_states, N_iters)

        print('Generating emission...')

        # Generate a 14-line sonnet in one long sequence of integers
        emission, states = HMM.generate_emission(140)

        sonnet_lines = [[] for i in range(14)]
        e = 0
        # Split the sonnet sequence into 14 lines
        for j in range(14):
            line_syllables = 0
            while line_syllables < 10:
                # Capitalize first word in every line
                if line_syllables == 0:
                    sonnet_lines[j].append(words_list[emission[e]].capitalize())
                # Append word to line
                else:
                    sonnet_lines[j].append(words_list[emission[e]])
                # Add number of syllables
                line_syllables += syllables[emission[e]][0]
                e += 1

        print('Naive Sonnet # ' + str(i))

        f = open('output/naive_poem.txt', 'a+')

        # Print the results.
        for k, line in enumerate(sonnet_lines):
            if k == 13:
                # Last line of sonnet ends with period.
                print(' '.join([word for word in line]) + '.')
                f.write(' '.join([word for word in line]) + '.')
            else:
                # Add some punctuation to the end of every sentence
                print(' '.join([word for word in line]) + random.choice([';', '.', ',',':', '!', '']))
                f.write(' '.join([word for word in line]) + random.choice([';', '.', ',',':', '!', '']))
            f.write('\n')
        f.write('\n\n')
        f.close()

    print('')
    print('')

def naive_poem2_generator(n_states, N_iters, k):
    '''
    Trains an HMM using unsupervised learning and generates k 14-line sonnets.

    Arguments:
        k:          Number of sonnets to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning (EM algorithm)
    '''
    # Data to train on from pre-processing
    # data, words_list, syllables, end_syllables = processed_shakespeare_data()
    data, words_list, syllables, end_syllables, rhyme_dict = processed_shakespeare_data2()

    # Generate k input sequences.
    for i in range(k):

        print('Training unsupervised HMM...')

        # Train the HMM.
        HMM = unsupervised_HMM(data, n_states, N_iters)

        print('Generating emission...')

        # Generate a 14-line sonnet in one long sequence of integers
        emission, states = HMM.generate_emission(140)

        sonnet_lines = [[] for i in range(14)]
        e = 0
        # Split the sonnet sequence into 14 lines
        for j in range(14):
            line_syllables = 0
            while line_syllables < 10:
                # Capitalize first word in every line
                if line_syllables == 0:
                    sonnet_lines[j].append(words_list[emission[e]].capitalize())
                # Append word to line
                else:
                    sonnet_lines[j].append(words_list[emission[e]])
                # Add number of syllables
                line_syllables += syllables[emission[e]][0]
                e += 1

        print('Naive Sonnet # ' + str(i))

        f = open('output/naive_poem2.txt', 'a+')

        # Print the results.
        for k, line in enumerate(sonnet_lines):
            if k == 13:
                # Last line of sonnet ends with period.
                print(' '.join([word for word in line]) + '.')
                f.write(' '.join([word for word in line]) + '.')
            else:
                # Add some punctuation to the end of every sentence
                print(' '.join([word for word in line]) + random.choice([';', '.', ',',':', '!', '']))
                f.write(' '.join([word for word in line]) + random.choice([';', '.', ',',':', '!', '']))
            f.write('\n')
        f.write('\n\n')
        f.close()

    print('')
    print('')

if __name__ == '__main__':
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format("Generating Sonnets with Naive Poem Generator"))
    print("#" * 70)
    print('')
    print('')

    n_states = 20
    N_iters = 40
    k = 2

    naive_poem2_generator(n_states, N_iters, k)
    # naive_poem2_generator(n_states, N_iters,l)
