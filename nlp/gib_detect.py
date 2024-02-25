#!/usr/bin/python

import pickle
import gib_detect_train

def check_word(wordList):
	'''Returns count of gibberish present in the list of words'''
	model_data = pickle.load(open('gib_model.pki', 'rb'))
	model_mat = model_data['mat']
	threshold = model_data['thresh']
	count = 0
	for word in wordList:
		l = word
		if gib_detect_train.avg_transition_prob(l, model_mat) <= threshold:
			count += 1
	return count