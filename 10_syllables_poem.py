from HMM import unsupervised_HMM
from preprocessing import processed_shakespeare_data2
import random
from preprocessing import punctuation_freq_shakespeare

def ten_syllables_poem_generator(n_states, N_iters, k):
    '''
    Trains an HMM using unsupervised learning and generates k 14-line sonnets.

    Arguments:
        k:          Number of sonnets to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning (EM algorithm)
    '''
    # Data to train on from pre-processing
    data, words_list, syllables, end_syllables, rhyme_dict = processed_shakespeare_data2()

    # Generate k input sequences.
    for i in range(k):

        print('Training unsupervised HMM...')

        # Train the HMM.
        HMM = unsupervised_HMM(data, n_states, N_iters)

        print('Generating emission...')

        # Generate a 14-line sonnet in one long sequence of integers
        sonnet_lines = HMM.generate_sonnet_emission(words_list, syllables, end_syllables)
        punct_marks, punct_freq = punctuation_freq_shakespeare()

        print('Sonnet # ' + str(i))

        f = open('output/10_syllables_poem.txt', 'a+')

        # Print the results.
        for s, emission in enumerate(sonnet_lines):
            if s == 13:
                # Last line of sonnet ends with period.
                print(' '.join([words_list[j] for j in emission]).capitalize() + '.')
                f.write(' '.join([words_list[j] for j in emission]).capitalize() + '.')
            else:
                # Add some punctuation to the end of every sentence
                # TODO: choose punctuation with  same probabilities as in original sonnets
                print(' '.join([words_list[j] for j in emission]).capitalize() + random.choices(punct_marks, weights=punct_freq)[0])
                f.write(' '.join([words_list[j] for j in emission]).capitalize() + random.choices(punct_marks, weights=punct_freq)[0])
            f.write('\n')
        f.write('\n\n')
        f.close()

    print('')
    print('')

if __name__ == '__main__':
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format("Generating Sonnets with 10-Syllable Lines"))
    print("#" * 70)
    print('')
    print('')

    n_states = 20
    N_iters = 40
    k = 2

    # Need to use gridsearch to find ideal number of hidden states
    ten_syllables_poem_generator(n_states, N_iters, k)
