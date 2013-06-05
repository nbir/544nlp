# -*- coding: utf-8 -*-

# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE
#
#
# FUNCTIONS:
#	==========
#	CharNgram(n)
#			Initialize n for character n-gram
#	gram_word(word)
# 		Finds list of character n-grams for word
#	gram_words(words)
# 		Finds list of character n-grams for all word in list words
#	gram_sent(sent)
# 		Splits sentence sent into words and finds list of character
#			n-grams for all word in sentence


import re


class CharNgram:
	#	Length of character n-gram
	# n = <integer>

	def __init__(self, n):
		self.n = n

	def gram_word(self, word):
	# Finds list of character n-grams for word
		grams = []
		if len(word) != 0:
			word = '#' + word.strip() + '#'
			if len(word) <= self.n:
				grams.append(word)
			else:
				for i in range(0, len(word)-self.n+1):
					grams.append(word[i:i+self.n])
		return grams


	def gram_words(self, words):
	# Finds list of character n-grams for all word in list words
		words = [word.strip() for word in words]
		return self.gram_word('#'.join(words))

	def gram_sent(self, sent, only_alpha=True):
	# Splits sentence sent into words and finds list of character
	#	n-grams for all word in sentence
		if only_alpha:
			sent = re.sub(r'[^a-zA-Z\s]+', '', sent)
			sent = sent.lower()
		words = sent.split()
		return self.gram_words(words)

	def test(self):
		#self.n = 4
		sent = 'hello  the, is arn\'t l_c_d a?'
		print 'Sentence: ' + sent
		print 'Character %s-grams : %s' % (self.n, ', '.join(self.gram_sent(sent)))
