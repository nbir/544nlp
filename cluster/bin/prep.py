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

from urllib import urlopen
import re
import nltk
from nltk import bigrams
from bs4 import BeautifulSoup as BS
import anyjson

def clean_html_docs(name):
	# Clean HTML from document and store in _cleaned folder
	name = name.replace(' ', '_')

	doc_path = 'data/' + my.DATA_FOLDER + 'webpages/' + name + '/raw/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')
	for doc_id in doc_names:
		doc = urlopen(doc_path + doc_id + '/index.html').read()
		raw = nltk.clean_html(doc)
		decoded = raw.decode('utf-8', errors='ignore')
		raw = decoded.encode('utf-8')
			
		out_dir = 'data/' + my.DATA_FOLDER + '_cleaned/' + name + '/'
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		with open(out_dir + doc_id, 'w') as fp1:
			fp1.write(raw)


def tokenize_docs(name, stopwords=True):
	# Tokenizes words, removes stopwords, adds POS tags and stores in _tokenized folder
	doc_path = 'data/' + my.DATA_FOLDER + '_cleaned/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			raw = fp1.read()
		sentences = nltk.sent_tokenize(raw)
		sentences = [s.replace('\n', '').replace('\r', '').strip() for s in sentences]
		sentences = [nltk.word_tokenize(s) for s in sentences]
		sentences = [nltk.pos_tag(s) for s in sentences]

		sentences = [[w for w in s if re.search('[a-zA-Z0-9]', w[0])] for s in sentences]
		sentences = [[w for w in s if w[0].lower() not in my.STOPWORDS] for s in sentences] if stopwords else sentences

		out_dir = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		with open(out_dir + doc_id, 'w') as fp1:
			fp1.write(anyjson.dumps(sentences))


def generate_lexicons(name):
	# Generate lexicons
	_generate_lex_unigram(name)
	_generate_lex_bigram(name)
	_generate_lex_unigram_pos(name)
	_generate_lex_stemmed(name)
	_generate_lex_stemmed_pos(name)
	_generate_lex_noun_verb(name)

def	_generate_lex_unigram(name):
	# Generate unigram lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent] for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	fdist = nltk.FreqDist(lexicon)
	
	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_unigram', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))

def	_generate_lex_bigram(name):
	# Generate bigram lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent] for sent in sentences]
		sentences = [bigrams(sent) for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	lexicon = ['%s__%s' % bigram for bigram in lexicon]
	fdist = nltk.FreqDist(lexicon)

	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_bigram', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))

def	_generate_lex_unigram_pos(name):
	# Generate unigram with POS tag lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [['%s__%s' % (token[0].lower(), token[1]) for token in sent] for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	fdist = nltk.FreqDist(lexicon)

	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_unigram_pos', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))

def	_generate_lex_stemmed(name):
	# Generate stemmed unigram lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	porter = nltk.PorterStemmer()
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[porter.stem(token[0]).lower() for token in sent] for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	fdist = nltk.FreqDist(lexicon)

	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_stemmed', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))

def	_generate_lex_stemmed_pos(name):
	# Generate stemmed unigram lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	porter = nltk.PorterStemmer()
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [['%s__%s' % (porter.stem(token[0]).lower(), token[1]) for token in sent] for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	fdist = nltk.FreqDist(lexicon)

	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_stemmed_pos', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))

def	_generate_lex_noun_verb(name):
	# Generate unigram lexicon
	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	lexicon = []
	for doc_id in doc_names:
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent if token[1] in my.NOUN_VERB_POS_TAGS] for sent in sentences]
		[lexicon.extend(sent) for sent in sentences]
	fdist = nltk.FreqDist(lexicon)

	fdist = dict([(key, fdist[key]) for key in list(fdist) if fdist[key]>1])

	out_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'lexicon_noun_verb', 'w') as fp1:
		fp1.write(anyjson.dumps(fdist))
