# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE
# 
#	Adapted from code by: Chris Potts
#	URL: http://compprag.christopherpotts.net/wordnet.html

import os
import sys
import re
import codecs
try:
	import nltk
	from nltk.corpus import wordnet
except ImportError:
	sys.stderr.write('NLTK not available, or NLTK datasets not available.')
	sys.exit(2)


class LexiconSA:
#	build(filename='lib/SentiWordNet.txt')
#			Builds a dictionary for lookup using SentiWordNet
#	senti_word(word)
# 		Calculates average [p, n, o] for given word over all synsets
#	senti_words(words)
# 		Calculates average [p, n, o] for all words
#	senti_sent(sent)
# 		Splits sentence into words and calculates average 
#			[p, n, o] for all words

	# Default StopWord list
	STOPWORDS = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
	#	Lookup database
	# db = {(pos, offset) : (positive, negative),
	#				...}

	def __init__(self):
		self.db = {}

	def build(self, filename='lib/SentiWordNet.txt'):
	# Builds a dictionary for lookup using SentiWordNet
		lines = codecs.open(filename, "r", "utf8").read().splitlines()
		lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
		for i, line in enumerate(lines):
			fields = re.split(r"\t+", line)
			fields = map(unicode.strip, fields)
			try:            
				pos, offset, pos_score, neg_score, synset_terms, gloss = fields
			except:
				sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
			if pos and offset:
				offset = int(offset)
				self.db[(pos, offset)] = (float(pos_score), float(neg_score))

	def senti_word(self, word):
	# Calculates average [p, n, o] for given word over all synsets
		p, n, o = 0.0, 0.0, 0.0
		synset_list = wordnet.synsets(word)
		for synset in synset_list:
			pos = synset.pos
			offset = synset.offset
			if (pos, offset) in self.db:
				pos_score, neg_score = self.db[(pos, offset)]
				p += pos_score
				n += neg_score
				o += (1.0 - (pos_score + neg_score))
		if sum([p,n,o]) != 0:
			return [round(val/sum([p,n,o]), 3) for val in [p, n, o]]
		return [p, n, o]

	def senti_words(self, words):
	# Calculates average [p, n, o] for all words
		p, n, o = 0.0, 0.0, 0.0
		for word in words:
			senti = self.senti_word(word)
			p += senti[0]
			n += senti[1]
			o += senti[2]
		if sum([p,n,o]) != 0:
			return [round(val/sum([p,n,o]), 3) for val in [p, n, o]]
		return [p, n, o]

	def senti_sent(self, sent):
	# Splits sentence into words and calculates average 
	#	[p, n, o] for all words
		words = nltk.word_tokenize(sent)
		words = [w for w in words if w.lower() not in self.STOPWORDS]
		return self.senti_words(words)

	def test(self):
		self.build()
		sent = 'What the bloody hell is wrong with you?'
		print 'Sentence: ' + sent
		p, n, o = self.senti_sent(sent)
		print 'Positive = %5s, Negative = %5s, Objective = %5s' % (p, n, o)
