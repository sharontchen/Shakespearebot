from HMM import unsupervised_HMM
from preprocessing import processed_shakespeare_data2
import random
from preprocessing import punctuation_freq_shakespeare

def haiku_generator(n_states, N_iters, k):
    '''
    Trains an HMM using unsupervised learning and generates k haikus.

    Arguments:
        k:          Number of haikus to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning
                    (EM algorithm)
    '''
    # Data to train on from pre-processing
    data, words_list, syllables, end_syllables, rhyme_dict, stress_dict = \
    processed_shakespeare_data2()

    print('Training unsupervised HMM...')

    # Train the HMM.
    HMM = unsupervised_HMM(data, n_states, N_iters)

    # Generate k input sequences.
    for i in range(k):

        print('Generating emission...')

        # Generate a 3-line poem in form of a haiku
        haiku_lines = HMM.generate_haiku_emission(words_list, syllables, \
        end_syllables)
        punct_marks, punct_freq = punctuation_freq_shakespeare()

        print('Haiku # ' + str(i))

        f = open('output/haiku_poem.txt', 'a+')

        # Print the results.
        for s, emission in enumerate(haiku_lines):
            if s == 2:
                # Last line of haiku ends with period.
                line = ' '.join([words_list[j] for j in emission])+ '.'
                line = line[0].upper() + line[1:]
                print(line)
                f.write(line)
            else:
                # Add some punctuation to the end of every sentence
                line = ' '.join([words_list[j] for j in emission]) + \
                random.choices(punct_marks, weights=punct_freq)[0]
                line = line[0].upper() + line[1:]
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
    print("{:^70}".format("Generating Haikus"))
    print("#" * 70)
    print('')
    print('')

    n_states = 20
    N_iters = 40
    k = 10

    # Need to use gridsearch to find ideal number of hidden states
    haiku_generator(n_states, N_iters, k)
