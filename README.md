# CS 155 Miniproject 3: Shakespearebot 5000

In this project, we attempt to generate Shakespearean sonnets by training various models on the entire corpus of Shakespeare’s sonnets. We tested the naive Hidden Markov Model (HMM) and improved it by constraining the model to fit the iambic pentameter and rhyming scheme of a Shakespearean sonnet. We also tried poem generation with recurrent neural networks (character-based LSTM) model and compared our results.

We use the following modules:

## Requirements
- Python 3  
- python-Levenshtein==0.12.0  
- Keras  
- numpy
- matplotlib

##  Poetry-Tools
Github Repository: https://github.com/hyperreality/Poetry-Tools

- Performs prosodic analysis of poetry.  
- Estimates rhyme scheme and metre using CMUDict, compares them against common forms using Levenshtein distance, and combines the results to guess the form of the poem.  
- Contains a rhymes function that is faster than any other I have found.
