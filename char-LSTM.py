from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io

with open("data/shakespeare.txt",'r') as f:
	text = f.read()
print('corpus length: ', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
units = 128
epoch_num = 60


model = Sequential()
model.add(LSTM(units, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
with open('char-LSTM-log-5.txt', 'a') as f:
	f.write('units: ' + str(units))
	f.write('\nstep: ' + str(step))
	f.write('\nepochs: ' + str(epoch_num))



def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def on_epoch_end(epoch, logs):
    # Function invoked at end of each epoch. Prints generated text.
    with open('char-LSTM-log-5.txt', 'a') as f:
	    print()
	    print('----- Generating text after Epoch: %d' % epoch)
	    f.write('\n----- Generating text after Epoch: %d' % epoch)

	    start_index = random.randint(0, len(text) - maxlen - 1)
	    for diversity in [0.25, 0.75, 1.5]:
	        print('----- diversity:', diversity)
	        f.write('\n----- diversity:' + str(diversity))

	        generated = ''
	        sentence = text[start_index: start_index + maxlen]
	        if epoch == 0:
	        	sentence = 'shall i compare thee to a summer\'s day?\n'
	        generated += sentence
	        print('----- Generating with seed: "' + sentence + '"')
	        f.write('\n----- Generating with seed: "' + sentence + '"')
	        sys.stdout.write(generated)
	        f.write('\n' + generated)

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

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model_history = model.fit(x, y,
          batch_size=units,
          epochs=epoch_num,
          callbacks=[print_callback])

with open('char-LSTM-log-5.txt', 'a') as f:
	losses = model_history.history['loss']
	min_loss = min(losses)
	min_iter = losses.index(min_loss)
	f.write('\nmin loss: ' + str(min_loss))
	f.write('\nmin loss epoch: ' + str(min_iter))