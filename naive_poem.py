from HMM import unsupervised_HMM
from preprocessing import processed_shakespeare_data

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
        # x = ''.join([str(i) for i in emission])

        sonnet_lines = [[] for i in range(14)]
        e = 0
        # Split the sonnet sequence into 14 lines
        for j in range(14):
            line_syllables = 0
            while line_syllables < 10:
                sonnet_lines[j].append(words_list[emission[e]])
                line_syllables += syllables[words_list[emission[e]]][0]
                e += 1

        print('Naive Sonnet # ' + str(i))

        f = open('output/naive_poem.txt', 'a+')

        # Print the results.
        for line in sonnet_lines:
            print(' '.join([word for word in line]))
            f.write(' '.join([word for word in line]))
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

    # Need to use gridsearch to find ideal number of hidden states
    naive_poem_generator(n_states, N_iters, k)
