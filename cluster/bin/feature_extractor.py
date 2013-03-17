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


def generate_feature_mat(name):
	# Generate feature matrix
	_generate_mat_unigram(name)
	_generate_mat_bigram(name)
	_generate_mat_unigram_pos(name)
	_generate_mat_stemmed(name)
	_generate_mat_stemmed_pos(name)
	_generate_mat_noun_verb(name)

def	_generate_mat_unigram(name):
	# Generate unigram feature matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_unigram', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent] for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'unigram', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))

def	_generate_mat_bigram(name):
	# Generate bigram feature matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_bigram', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent] for sent in sentences]
		sentences = [bigrams(sent) for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		doc = ['%s__%s' % bigram for bigram in doc]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'bigram', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))


def	_generate_mat_unigram_pos(name):
	# Generate unigram with POS tag feature matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_unigram_pos', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [['%s__%s' % (token[0].lower(), token[1]) for token in sent] for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'unigram_pos', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))


def	_generate_mat_stemmed(name):
	# Generate stemmed unigram featuer matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_stemmed', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	porter = nltk.PorterStemmer()
	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[porter.stem(token[0]).lower() for token in sent] for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'stemmed', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))

def	_generate_mat_stemmed_pos(name):
	# Generate stemmed unigram feature matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_stemmed_pos', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	porter = nltk.PorterStemmer()
	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [['%s__%s' % (porter.stem(token[0]).lower(), token[1]) for token in sent] for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'stemmed_pos', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))


def	_generate_mat_noun_verb(name):
	# Generate unigram feature matrix
	lex_dir = 'data/' + my.DATA_FOLDER + '_lexicon/' + name + '/'
	with open(lex_dir + 'lexicon_noun_verb', 'r') as fp1:
		lexicon = anyjson.loads(fp1.read())

	doc_path = 'data/' + my.DATA_FOLDER + '_tokenized/' + name + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	mat = []
	for doc_id in doc_names:
		doc = []
		with open(doc_path + doc_id, 'r') as fp1:
			sentences = anyjson.loads(fp1.read())
		sentences = [[token[0].lower() for token in sent if token[1] in my.NOUN_VERB_POS_TAGS] for sent in sentences]
		[doc.extend(sent) for sent in sentences]
		fdist = nltk.FreqDist(doc)
		row = [fdist[token] if token in fdist else 0 for token in lexicon]
		mat.append(row)

	out_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + 'noun_verb', 'w') as fp1:
		fp1.write(anyjson.dumps(mat))



