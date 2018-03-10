from HMM import unsupervised_HMM
from preprocessing import processed_shakespeare_data
from preprocessing import processed_shakespeare_data2
import random
from preprocessing import punctuation_freq_shakespeare

def ten_syllables_rhyme_generator(n_states, N_iters, k, train_on='line'):
    '''
    Trains an HMM using unsupervised learning and generates k 14-line sonnets.

    Arguments:
        k:          Number of sonnets to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning
                    (EM algorithm)
        train_on:   Optional argument. Train on either line or sonnet.
                    Default to line.
    '''
    # Data to train on from pre-processing.
    data, words_list, syllables, end_syllables, rhyme_dict, stress_dict = \
    processed_shakespeare_data2()

    # If train on sonnet instead of line.
    if train_on == 'sonnet':
        data, words_list, syllables, end_syllables = \
        processed_shakespeare_data()

    print('Training unsupervised HMM...')

    f = open('output/10_syllables_rhyme.txt', 'a+')

    print('(%d states, %d iterations, training on each %s)\n\n' % \
    (n_states, N_iters, train_on))
    f.write('(%d states, %d iterations, training on each %s)\n\n\n' % \
    (n_states, N_iters, train_on))

    # Train the HMM.
    HMM = unsupervised_HMM(data, n_states, N_iters)

    # Generate k input sequences.
    for i in range(k):

        # Generate a 14-line sonnet
        sonnet_lines = HMM.generate_sonnet_rhyme(words_list, syllables, \
        end_syllables, rhyme_dict)
        punct_marks, punct_freq = punctuation_freq_shakespeare()

        print('\n\nSonnet # ' + str(i + 1))

        # Print the results.
        for s, emission in enumerate(sonnet_lines):
            if s == 13:
                # Last line of sonnet ends with period.
                line = ' '.join([words_list[j] for j in emission])+ '.'
                line = line[0].upper() + line[1:]
                print(line)
                f.write(line)
            else:
                line = ' '.join([words_list[j] for j in emission]) + \
                random.choices(punct_marks, weights=punct_freq)[0]
                line = line[0].upper() + line[1:]
                # Add some punctuation to the end of every sentence
                print(line)
                f.write(line)
            f.write('\n')
        f.write('\n\n')

    f.close()

    print('')
    print('')

if __name__ == '__main__':
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format("Generating Rhyming Sonnets with 10-Syllable Lines"))
    print("#" * 70)
    print('')
    print('')

    n_states = 100
    N_iters = 20
    k = 3

    ten_syllables_rhyme_generator(n_states, N_iters, k, train_on='line')
