import preprocessing as pp

X, dictionary, syllables, end_syllables = pp.processed_shakespeare_data()
print(X)
print(dictionary[1109])
