# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import settings as my
from lib.sentiwordnet import *
from lib.charngram import *

from collections import Counter
from bs4 import BeautifulSoup as BS
import re
import pickle
import csv
from pprint import pprint

import numpy
from sklearn.feature_extraction.text import CountVectorizer

## TEXT features
def gen_text_feat():
	corpus = []
	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text_bal.txt', 'rb') as fp_text:
		cr_text = csv.reader(fp_text, delimiter='~')
		for row in cr_text:
			text = row[0]
			text = re.sub(r'[^a-zA-Z\s]+', '', text)
			text = text.lower()
			corpus.append(text)

	vectorizer = CountVectorizer(min_df=my.MIN_WORD_COUNT)
	X = vectorizer.fit_transform(corpus)
	X = X.toarray().tolist()
	feats = vectorizer.get_feature_names()
	print 'Number of word unigram features = %s' % len(feats)
	
	fp_out = open('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_unigram.csv', 'wb')
	cw_out = csv.writer(fp_out, delimiter=',')
	cw_out.writerow(feats)
	for row in X:
		cw_out.writerow(row)


## CHARACTER N-GRAM features
def gen_char_feat():
	cng3 = CharNgram(3)
	cng4 = CharNgram(4)
	corpus = []

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text_bal.txt', 'rb') as fp_text:
		cr_text = csv.reader(fp_text, delimiter='~')
		for row in cr_text:
			text = row[0]
			corpus.append(' '.join(cng3.gram_sent(text) + cng4.gram_sent(text)))

	vectorizer = CountVectorizer(min_df=my.MIN_CWORD_COUNT)
	X = vectorizer.fit_transform(corpus)
	X = X.toarray().tolist()
	feats = vectorizer.get_feature_names()
	print 'Number of character n-gram features = %s' % len(feats)
	
	fp_out = open('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_charngram.csv', 'wb')
	cw_out = csv.writer(fp_out, delimiter=',')
	cw_out.writerow(feats)
	for row in X:
		cw_out.writerow(row)


## sENTIwORDnET feature
def gen_swn_feat():
	lex = LexiconSA()
	lex.build()

	fp_out = open('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_sentiwordnet.csv', 'wb')
	cw_out = csv.writer(fp_out, delimiter=',')
	feats = ['POSITIVITY', 'NEGATIVITY', 'OBJECTIVITY']
	cw_out.writerow(feats)
	print 'Number of SentiWordNet features = %s' % len(feats)

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text_bal.txt', 'rb') as fp_text:
		cr_text = csv.reader(fp_text, delimiter='~')
		for row in cr_text:
			text = row[0]
			pno = lex.senti_sent(text)
			cw_out.writerow(pno)



## AUDIO features
def gen_audio_feat():
	fp_out = open('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_audio.csv', 'wb')
	cw_out = csv.writer(fp_out, delimiter=',')
	feats = ['PITCH_MIN', 'PITCH_MAX', 'PITCH_RANGE', 'PITCH_MEAN', 'PITCH_SD', 'PITCH_MAS', \
					'INTENSITY_MIN', 'INTENSITY_MAX', 'INTENSITY_RANGE', 'INTENSITY_MEAN', 'INTENSITY_SD', 'INTENSITY_RMS']
	cw_out.writerow(feats)
	print 'Number of Audio features = %s' % len(feats)

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'Xy_info_bal.csv', 'rb') as fp_info:
		cr_info = csv.reader(fp_info, delimiter=',')
		for row in cr_info:
			fname, start, end = row
			start, end = float(start), float(end)
			#print '%8s %8s %8s' % (fname, start, end)
			p = []
			i = []
			with open('data/' + my.DATA_FOLDER  + '_praat/' + my.PRAAT_FILE_FORMAT % fname, 'rb') as fp_praat:
				cr = csv.reader(fp_praat, delimiter=',')
				for row in cr:
					time, pitch, intensity = row
					time, pitch, intensity = float(time), float(pitch), float(intensity)
					if time >= start and time <= end:
						p.append(float(pitch))
						i.append(float(intensity))
						if time > end:
							break

				# Pitch features
				#length = len(p)
				p = [val for val in p if val > 0]
				if len(p) == 0:
					vec = [0]*6
				else:
					minn, maxn, mas = min(p), max(p), MAS(p)
					rng = round(maxn - minn, 3)
					p = numpy.array(p)
					mean, sd = round(p.mean(), 3), round(p.std(), 3)
					vec = [minn, maxn, rng, mean, sd, mas]
				
				#Intensity features
				i = [val for val in i if val > 0]
				if len(i) == 0:
					vec.extend([0]*6)
				else:
					minn, maxn, rms = min(i), max(i), RMS(i)
					rng = round(maxn - minn, 3)
					i = numpy.array(i)
					mean, sd = round(i.mean(), 3), round(i.std(), 3)
					vec.extend([minn, maxn, rng, mean, sd, rms])

				cw_out.writerow(vec)
	fp_out.close()
		
def MAS(l):
# calculate Mean Absolute Slope of the list
	slopes = []
	for i in range(1, len(l)-1):
		slopes.append(abs(l[i]-l[i+1]))
	return round(sum(slopes)/len(slopes), 3) if len(slopes) != 0 else 0
def RMS(l):
# calculates Root Mean Square of the list
	return round(numpy.sqrt(numpy.mean(numpy.array(l)**2)), 3) if len(l) != 0 else 0


## LABELS
def gen_labels():
	fp_out = open('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'y.csv', 'wb')

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'y_bal.csv', 'rb') as fp_y:
		fp_out.write('CLASS\n' + fp_y.read())

