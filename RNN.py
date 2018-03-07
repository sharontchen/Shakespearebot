import tensorflow as tf 
import keras
import numpy as np
import preprocessing as pp

def get_data():
	sonnets = pp.load_shakespeare()
	words = pp.load_syllable_dict()
	data = pp.process_data(sonnets)
	return data, words

def main():
	print("Processing data...")
	data, words = get_data()
	print("Processed data")

if __name__ == '__main__':
	main()