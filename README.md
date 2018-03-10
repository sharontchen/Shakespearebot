# CS 155 Miniproject 3: Shakespearebot 5000

In this project, we attempt to generate Shakespearean sonnets by training a Hidden Markov Model (HMM) on the entire corpus of Shakespeare’s sonnets.

We use the following modules:

##  Poetry-Tools
Github Repository: https://github.com/hyperreality/Poetry-Tools

Performs prosodic analysis of poetry.
Estimates rhyme scheme and metre using CMUDict, compares them against common forms using Levenshtein distance, and combines the results to guess the form of the poem.
Contains a rhymes function that is faster than any other I have found.
