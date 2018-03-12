'''
Code adapted from Kera's example lstm for text generation:
https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py
'''
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Read the input text file as a single string
with open("data/shakespeare.txt",'r') as f:
	text = f.read()

# Remove all double newlines and numbers from text
text = list(text)
j = text
i = 1
k = []
while i < len(j):
    if j[i-1] == '\n' and j[i] == '\n' and j[i + 1] == '\n':
        i += 23
    if j[i-1:i+2] == [' ', ' ', ' ']:
        i += 20
    k.append(j[i])
    i+=1
text = ''.join(k)
print('corpus length: ', len(text))
j, i, k = 0,0,0

# Get all unique characters in the text, assign them unique integers
chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# Cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []

# Generate all possible sentences in the file that are length maxlen
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

# Vectorize sentences
print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# Set parameters
char_len = len(chars)
u_list = [200]
epoch_num = 100
optimizer = 'rmsprop'
temperatures = [0.25, 0.5, 0.75, 1, 1.5]
n_poems = 100

loss_list = []

for units in u_list:
	print('Building model...')

	model = Sequential()
	model.add(LSTM(units, input_shape=(maxlen, char_len)))
	model.add(Dense(char_len))
	model.add(Activation('softmax'))

	model.compile(loss='categorical_crossentropy', optimizer=optimizer)
	with open('char-LSTM-log-11.txt', 'a') as f:
		f.write('\nunits: ' + str(units))
		f.write('\nstep: ' + str(step))
		f.write('\nepochs: ' + str(epoch_num))
		f.write('\noptimizer: ' + str(optimizer))

	model_history = model.fit(x, y,
	          batch_size=units,
	          epochs=epoch_num)

	with open('char-LSTM-log-11.txt', 'a') as f:
		losses = model_history.history['loss']
		min_loss = min(losses)
		min_iter = losses.index(min_loss)
		f.write('\nmin loss: ' + str(min_loss))
		f.write('\nmin loss epoch: ' + str(min_iter))

	loss_list.append(losses)

# Generate poems with trained model with given seed 
sample_count = 0
with open('char-LSTM-log-11.txt', 'a') as f:
	while sample_count < n_poems:
		if sample_count == 0:
			print('\n----- Comparing different temperatures with same initial seed -----')
			f.write('\n----- Comparing different temperatures with same initial seed -----')
		for diversity in temperatures:
		    print('----- diversity:', diversity)
		    f.write('\n----- diversity:' + str(diversity))

		    start_index = random.randint(0, len(text) - maxlen - 1)
		    generated = ''
		    sentence = text[start_index: start_index + maxlen]
		    if sample_count == 0:
		    	sentence = 'shall i compare thee to a summer\'s day?\n'
		    generated += sentence

		    print('----- Generating with seed: "' + sentence + '"')
		    f.write('\n----- Generating with seed: "' + sentence + '"')
		    sys.stdout.write(generated)
		    f.write('\n' + generated)

		    # Predict next character
		    for i in range(560):
		        x_pred = np.zeros((1, maxlen, len(chars)))
		        for t, char in enumerate(sentence):
		            x_pred[0, t, char_indices[char]] = 1.

		        preds = model.predict(x_pred, verbose=0)[0]
		        next_index = sample(preds, diversity)
		        next_char = indices_char[next_index]

		        generated += next_char
		        sentence = sentence[1:] + next_char

		        sys.stdout.write(next_char)
		        f.write(next_char)
		        sys.stdout.flush()
		    print()
		sample_count+=1

'''
fig = plt.figure()
for i, loss in enumerate(loss_list):
    plt.plot(loss, label=str(u_list[i]) + ' units')
plt.title("Loss per epoch for different LSTM units")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.savefig('Loss-trends-different-LSTM-units.png')
'''