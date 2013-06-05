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
from lib.data import *
from lib.classifiers import *

from lxml import etree
from lxml import objectify
from bs4 import BeautifulSoup as BS
import csv
import re
from pprint import pprint

from sklearn import cross_validation
from sklearn import tree

def test():
	#lex = LexiconSA()
	#lex.test()
	#lex.build()
	#h = lex.senti_words(['slow', 'party', 'crack', 'car'])
	#h = lex.senti_sent('What the bloody hell is wrong with you?')
	#print h
	test_classify()	

def test_classify():
	c = Data()
	c.load_Xy('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_audio.csv', 'data/' + my.DATA_FOLDER  + '_feature_mat/' + 'y.csv')

	cv = cross_validation.StratifiedKFold(c.y, 10)
	clf = tree.DecisionTreeClassifier()
	scores = cross_validation.cross_val_score(clf, c.X, c.y, cv=cv, n_jobs=-1)
	print scores.mean(), scores.max()
	#pprint(s)

	#c.reorder()
	#c.fit_svm()
	#c.show_Xlen()
	#c.remove_feat('INTENSITY_MEAN')
	#c2 = Data()
	#c2.load_X('data/' + my.DATA_FOLDER  + '_feature_mat/' + 'X_sentiwordnet.csv')
	#c.extend_X(c2)
	#c.show_Xlen()
	#c.show_feat(1)
	#
	#c.show_y()
	#c.show_feat(1)
	#print c.get_feats()
	#print '#'*20
	#c.scale_feats()
	#c.show_feat(3)
	#c.reduce_pca()
	#c.show_Xlen()


	#cl = ClassifySVM(c)
	#cl.learn_param()
	#cl.choose_best_param()
	#cl.find_test_acc()
	#cl.plot_train('data/' + my.DATA_FOLDER + 'plots/' + 'svm_train_swn' + '.png')
	#cl.show_scores()


def do_classification(combi):
	name = combi
	obj_list = []
	Xy_dir = 'data/' + my.DATA_FOLDER  + '_feature_mat/'
	plot_dir = 'data/' + my.DATA_FOLDER  + 'plots/'

	for char in combi:
		new_obj = Data()
		new_obj.load_Xy(Xy_dir + my.FEAT_TYPE_MAP[char], Xy_dir + 'y.csv')
		obj_list.append(new_obj)
	print name, len(obj_list)
	
	for data in obj_list:
		data.scale_feats()
		data.reduce_pca()

	data = obj_list.pop()
	for obj in obj_list:
		data.extend_X(obj)
	#data.scale_feats()

	svm = ClassifySVM(data)
	svm.learn()
	svm.plot_train(plot_dir + name + '.png')

	return svm.get_train_acc(), svm.get_test_acc()



def test_length():
	fp_y = open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'y.csv', 'rb')
	cr_y = csv.reader(fp_y, delimiter=',')

	a = []
	b = []

	with open('data/' + my.DATA_FOLDER  + '_cleaned/' + 'Xy_info.csv', 'rb') as fp_info:
		cr_info = csv.reader(fp_info, delimiter=',')
		for row in cr_info:
			fname, start, end = row
			y = int(cr_y.next()[0])
			if y == 0:
				a.append(round(float(end)-float(start),2))
			else:
				b.append(round(float(end)-float(start),2))
	a = sorted(a)
	b = sorted(b)
	print a
	print '\n'
	print b

def test_words():
	with open('data/' + my.DATA_FOLDER + 'corpus/amida/' + 'ED1002c.D.words.xml', 'rb') as fp1:
		raw = fp1.read()
	soup = BS(raw)

	for tag in soup.find_all('w'):
		w_id, start, end, text = tag['nite:id'], tag['starttime'], tag['endtime'], tag.text
		#print w_id, start, end, text
	for tag in soup.find_all('vocalsound'):
		if tag['type'] == 'laugh':
			print tag['nite:id']



def test_subj():
	re_stype = 'subj\-types\.xml\#id\(ami_subj(?P<stype>[0-9\.]*)\)'
	re_stype = re.compile(re_stype)
	re_words = '[a-zA-Z0-9]{7}\.[A-Z]\.words\.xml\#id\((?P<from>[a-zA-Z0-9\.]*)\)(\.\.id\((?P<to>[a-zA-Z0-9\.]*)\))?'
	re_words = re.compile(re_words)

	with open('data/' + my.DATA_FOLDER + 'corpus/amida/' + 'ED1005a.A.subjectivity.xml', 'rb') as fp1:
		raw = fp1.read()
	soup = BS(raw)

	for tag in soup.find_all('subj'):
		for sub in tag.find_all('nite:pointer'):
			print sub['href']
			match = re_stype.match(sub['href'])
			stype = match.group('stype')
			print stype

		for sub in tag.find_all('nite:child'):
			#print sub['href']
			match = re_words.match(sub['href'])
			from_w = match.group('from')
			to_w = match.group('to') if match.group('to') else from_w
			#print from_w, to_w

