# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import settings as my

from bs4 import BeautifulSoup as BS
import re
import pickle
import csv
import random
from pprint import pprint


def build_word_dict():
	words = {}
	laughs = {}

	doc_path = 'data/' + my.DATA_FOLDER + 'corpus/words/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	for doc in doc_names:
		with open(doc_path + doc, 'rb') as fp1:
			raw = fp1.read()
			soup = BS(raw)

			for tag in soup.find_all('w'):
				try:
					w_id, start, end, text = tag['nite:id'], tag['starttime'], tag['endtime'], tag.text
					words[w_id] = {'word': text, 'start': start, 'end': end}
				except:
					'Error reading word!'

			for tag in soup.find_all('vocalsound'):
				if tag['type'] == 'laugh':
					w_id, start, end = tag['nite:id'], tag['starttime'], tag['endtime']
					words[w_id] = {'word': 'LAUGH', 'start': start, 'end': end}
					#print start, end

	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'words.pickle', 'wb') as fp1:
		pickle.dump(words, fp1)
	#pprint(words)


def build_subj_list():
	re_stype = 'subj\-types\.xml\#id\(ami_subj(?P<stype>[0-9\.]*)\)'
	re_stype = re.compile(re_stype)
	re_words = '[a-zA-Z0-9]{7}\.[A-Z]\.words\.xml\#id\((?P<from>[a-zA-Z0-9\.]*)\)(\.\.id\((?P<to>[a-zA-Z0-9\.]*)\))?'
	re_words = re.compile(re_words)
	re_wno = '(?P<fname>ED1005[abc])\.(?P<spkr>[ABCD])\.words(?P<w_no>[0-9]*)'
	re_wno = re.compile(re_wno)
	wno_str = '%s.%s.words%s'

	subj_rows = []

	with open('data/' + my.DATA_FOLDER  + '_pickle/' + 'words.pickle', 'rb') as fp1:
		words = pickle.load(fp1)

	doc_path = 'data/' + my.DATA_FOLDER + 'corpus/subjectivity/'
	doc_names = os.listdir(doc_path)
	if '.DS_Store' in doc_names:
		doc_names.remove('.DS_Store')

	for doc in doc_names:
		with open(doc_path + doc, 'rb') as fp1:
			raw = fp1.read()
			soup = BS(raw)

			for tag in soup.find_all('subj'):
				for sub in tag.find_all('nite:pointer'):
					match = re_stype.match(sub['href'])
					stype = match.group('stype')

					if stype in my.CLASS_1 or stype in my.CLASS_2:
						for sub in tag.find_all('nite:child'):
							# From/To word ID
							match = re_words.match(sub['href'])
							from_w = match.group('from')
							to_w = match.group('to') if match.group('to') else from_w
							#print from_w, to_w

							# From/To word number
							match = re_wno.match(from_w)
							fname = match.group('fname')
							spkr = match.group('spkr')
							start = int(match.group('w_no'))
							match = re_wno.match(to_w)
							end = int(match.group('w_no'))
							
							# Form sentence by combining words in range
							sent = []
							for w_no in range(start, end+1):
								w_id = wno_str % (fname, spkr, w_no)
								if w_id in words:
									sent.append(words[w_id]['word'])
							sent = ' '.join(sent)
							#print sent
							
							# Utterence start/end time
							start = words[from_w]['start'] if from_w in words else words[wno_str % (fname, spkr, start+1)]['start']
							end = words[to_w]['end'] if to_w in words else words[wno_str % (fname, spkr, end-1)]['end']
							#print start, end

							# Class
							stype = 0 if stype in my.CLASS_1 else 1

							subj_rows.append([stype, sent, fname, start, end])
					break

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
			text = cr_text.next()[0]

			if y == 0:
				dur = round(float(end)-float(start),2)
				if dur < 16.55:
					a.append([fname, start, end, y, text])
			else:
				b.append([fname, start, end, y, text])

	# Shuffle and trim
	random.shuffle(a)
	a = a[0:len(b)]

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
		

