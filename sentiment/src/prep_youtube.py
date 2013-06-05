# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import os
import sys

import settings as my

from bs4 import BeautifulSoup as BS
import re
import pickle
import csv
import random
from pprint import pprint


def remane_files(folder, ext):
	re_fname = 'video(?P<v_no>[0-9]{1,2}).'
	re_fname = re.compile(re_fname)

	doc_path = 'data/' + my.DATA_FOLDER + 'corpus/' + folder + '/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	for doc in doc_names:
		match = re_fname.match(doc)
		v_no = match.group('v_no')
		fname = 'video_%s.' % v_no + ext
		os.rename(doc_path+doc, doc_path+fname)

def build_word_dict():
	re_time = 'time\=\"(?P<time>[0-9\.]*)\"'
	re_time = re.compile(re_time)
	words = {}

	doc_path = 'data/' + my.DATA_FOLDER + 'corpus/transcriptions/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	for doc in doc_names:
		v_no = int(doc.replace('video_','').replace('.trs',''))
		words[v_no] = []
		lines = []

		with open(doc_path + doc, 'rb') as fp1:
			for line in fp1.readlines():
				lines.append(line.strip())
		
			for i in range(0, len(lines)):
				line = lines[i]
				match = re_time.search(line)
				if match:
					time = match.group('time')
					words[v_no].append([time, lines[i+1]])

		
	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'words.pickle', 'wb') as fp1:
		pickle.dump(words, fp1)
	#pprint(words)

def build_utterence_list():
	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'words.pickle', 'rb') as fp1:
		words = pickle.load(fp1)
	
	subj_rows = []
	
	with open('data/' + my.DATA_FOLDER  + 'corpus/' + 'annotations.csv', 'rb') as fp1:
		cr_a = csv.reader(fp1, delimiter=',')
		_ = cr_a.next()
		for ant in cr_a:
			v_no, start, end, _, _, _, stype = ant
			v_no, start, end, stype = int(v_no), float(start), float(end), int(stype)
			
			if stype in [1, -1]:
				stype = 0 if stype == -1 else 1
				fname = 'video_%s' % v_no
				sent = []

				for row in words[v_no]:
					time, text = float(row[0]), row[1]
					if time >= start and time <= end:
						sent.append(text)
						if time >= end:
							break
				sent = ' '.join(sent)

				subj_rows.append([stype, sent, fname, start, end])

	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'subj_rows.pickle', 'wb') as fp1:
		pickle.dump(subj_rows, fp1)


def make_data_info():
	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'subj_rows.pickle', 'rb') as fp1:
		subj_rows = pickle.load(fp1)

	fp_y = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'y.csv', 'wb')
	cw_y = csv.writer(fp_y, delimiter=',')
	fp_info = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'Xy_info.csv', 'wb')
	cw_info = csv.writer(fp_info, delimiter=',')
	fp_txt = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text.txt', 'wb')

	for row in subj_rows:
		stype, sent, fname, start, end = row
		cw_y.writerow([stype])
		cw_info.writerow([fname, start, end])
		fp_txt.write(sent+'\n')
		

def balance_classes():
	fp_y = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'y.csv', 'rb')
	cr_y = csv.reader(fp_y, delimiter=',')

	fp_text = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text.txt', 'rb')
	cr_text = csv.reader(fp_text, delimiter='~')

	a = []
	b = []

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'Xy_info.csv', 'rb') as fp_info:
		cr_info = csv.reader(fp_info, delimiter=',')

		for row in cr_info:
			fname, start, end = row
			y = int(cr_y.next()[0])
			text = cr_text.next()
			if len(text) != 0 and len(text[0]) > 20:
				text = text[0]

				if y == 0:					
					a.append([fname, start, end, y, text])
				else:
					b.append([fname, start, end, y, text])

	# Shuffle and trim
	random.shuffle(a)
	a = a[0:len(b)]
	#print len(a), len(b)

	# Write balanced files
	fp_y = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'y_bal.csv', 'wb')
	cw_y = csv.writer(fp_y, delimiter=',')

	fp_text = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'rawX_text_bal.txt', 'wb')
	cw_text = csv.writer(fp_text, delimiter='~')

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'Xy_info_bal.csv', 'wb') as fp_info:
		cw_info = csv.writer(fp_info, delimiter=',')
		for row in a+b:
			fname, start, end, y, text = row
			cw_info.writerow([fname, start, end])
			cw_y.writerow([y])
			cw_text.writerow([text])
		

