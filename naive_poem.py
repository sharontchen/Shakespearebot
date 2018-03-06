from HMM import unsupervised_HMM

def naive_poem_generator(data, n_states, N_iters, k):
    '''
    Trains an HMM using unsupervised learning and generates 14-line sonnets.

    Arguments:
        k:          Number of sonnets to generate.
        n_states:   Number of hidden states that the HMM should have.
        N_iters:    Number of iterations for the unsupervised learning (EM algorithm)
    '''

    # Generate k input sequences.
    for i in range(k):

        # Train the HMM.
        HMM = unsupervised_HMM(data, n_states, N_iters)

        # Generate a 14-line sonnet
        words, states = HMM.generate_sonnet()
        x = ''.join([word for word in words])

        # Print the results.
        print("{:30}".format(x))

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

    n_states = 30
    N_iters = 500
    k = 5

    # Need data from pre-processing

    # Need to use gridsearch to find ideal number of hidden states
    naive_poem_generator(data, n_states, N_iters, k)
