# -*- coding: utf-8 -*-

# Web Page Clustering of Ambiguous Names - 544 NLP Assignment2
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE


import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import settings as my

import csv

def generate_results():
	directive = 'java -Xmx2048m -cp ' + \
		'lib/scorer_1.1/wepsEvaluation.jar ' + \
		'es.nlp.uned.weps.evaluation.SystemScorer ' + \
		'data/' + my.DATA_FOLDER + 'gold ' + \
		'data/' + my.DATA_FOLDER + 'output ' + \
		'data/' + my.DATA_FOLDER + 'results ' + \
		'-ALLMEASURES ' + \
		'-AllInOne -OneInOne -Combined ' + \
		'-overwrite'
	print directive

	os.system(directive)




################################################################################
def test3():
	import nltk
	from nltk.corpus import conll2000
	from urllib import urlopen

	fname = 'data/dummy/webpages/Abby_Watkins/raw/002/index.html'
	doc = urlopen(fname).read()
	raw = nltk.clean_html(doc)

	decoded = raw.decode('utf-8', errors='ignore')
	raw = decoded.encode('utf-8')
	print raw

	sentences = nltk.sent_tokenize(raw)
	sentences = [s.replace('\n', '').replace('\r', '').strip() for s in sentences]
	sentences = [nltk.word_tokenize(s) for s in sentences]
	sentences = [nltk.pos_tag(s) for s in sentences]
	#porter = nltk.PorterStemmer()
	#sentences = [[(porter.stem(w[0]), w[1]) for w in s] for s in sentences]
	#sentences = [[w[0] for w in s] for s in sentences]
	#sentences = [['%s_%s' % w for w in s] for s in sentences]


	lexicon = []
	#for s in sentences:
		#print len(s)
		#for w in s:
		#	print w[0]
		#print ' '.join(w[0] for w in s)
		#print nltk.ne_chunk(s, binary=True)

		#lexicon.extend(s)
	fdist = nltk.FreqDist(lexicon)
	#for w in fdist:
	#	print '%s\t%s' % (w, fdist[w])
	#print raw


def test2():
	from bs4 import BeautifulSoup as BS
	from urllib import urlopen

	fname = 'data/dummy/webpages/Abby_Watkins/raw/001/index.html'
	doc = urlopen(fname).read()

	soup = BS(doc, 'lxml')

	print soup.title.text







import nltk.chunk
import itertools

class TagChunker(nltk.chunk.ChunkParserI):
	def __init__(self, chunk_tagger):
		self._chunk_tagger = chunk_tagger

	def parse(self, tokens):
		# split words and part of speech tags
		(words, tags) = zip(*tokens)
		# get IOB chunk tags
		chunks = self._chunk_tagger.tag(tags)
		# join words with chunk tags
		wtc = itertools.izip(words, chunks)
		# w = word, t = part-of-speech tag, c = chunk tag
		lines = [' '.join([w, t, c]) for (w, (t, c)) in wtc if c]
		# create tree from conll formatted chunk lines
		return nltk.chunk.conllstr2tree('\n'.join(lines))


