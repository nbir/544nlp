# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import settings as my
from lib.data import *
from lib.classifiers import *

import csv
from pprint import pprint
import matplotlib.pyplot as plt


def classify_all():
	combis = ['T','C','S','A','TC','TS','TA','CS','CA','SA','TCS','TCA','TSA','CSA','TCSA',]
	acc = []
	plot_dir = 'data/' + my.DATA_FOLDER  + 'plots/'

	#fp_svm = open(plot_dir + 'results_svm_early.csv', 'wb')
	#cw_svm = csv.writer(fp_svm, delimiter=',')
	#fp_dt = open(plot_dir + 'results_dt_early.csv', 'wb')
	#cw_dt = csv.writer(fp_dt, delimiter=',')
	fp_rf = open(plot_dir + 'results_rf_early.csv', 'wb')
	cw_rf = csv.writer(fp_rf, delimiter=',')

	for combi in combis:
		#train, test = do_svm(combi)
		#cw_svm.writerow([combi, train, test])
		#train = do_dt(combi)
		#cw_dt.writerow([combi, train])
		train = do_rf(combi)
		cw_rf.writerow([combi, train])


def do_svm(combi):
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


def do_dt(combi):
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

	dt = ClassifyDT(data)
	dt.learn()

	return dt.get_train_acc()


def do_rf(combi):
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

	rf = ClassifyRF(data)
	rf.learn()

	return rf.get_train_acc()


def plot_charts():
	ami = [{'name' 		: 'SVM - AMI corpus',
					'labels' 	: ['unigram', 'audio', 'char n-grams', 'char n-grams\n + audio'],
					'y_vals' 	: [0.5224, 0.5224, 0.6418, 0.6716]},

					{'name' 	: 'Training acc. - AMI corpus',
					'labels' 	: ['SVM\n (SA)', 'Random\nForest (CSA)', 'Decision\nTree (TCSA)'],
					'y_vals' 	: [0.6634, 0.7692, 0.7778]}
					]
	yt =	[{'name' 		: 'SVM - Youtube ds.',
					'labels' 	: ['unigram', 'SentiWordNet', 'audio', 'unigram + \nchar n-grams\n + audio'],
					'y_vals' 	: [0.5526, 0.5526, 0.5526, 0.6053]},

					{'name' 	: 'Training acc. - Youtube ds.',
					'labels' 	: ['SVM\n (TCA)', 'Random\nForest (TCA)', 'Decision\nTree (T SA)'],
					'y_vals' 	: [0.6697, 0.8, 0.75]},\
				] 

	if my.DATA_FOLDER == 'amida/':
		for d in ami:
			plot_bar_for(d)
	else:
		for d in yt:
			plot_bar_for(d)


def plot_bar_for(data):
	colors = ["#3B3B3B","#FA71AF","#FF7F00","#377EB8","#4DAF4A","#984EA3","#E41A1C","#A65628"]

	ind = numpy.arange(len(data['labels']))  # the x locations for the groups
	width = 0.5       # the width of the bars
	fig = plt.figure(figsize=(4,5))
	ax = fig.add_subplot(111)
	ax.set_autoscaley_on(False)
	ax.set_ylim([0,1])
	ax.set_title(data['name'])
	plt.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.28)

	for i in range(0, len(data['labels'])):
		color = colors.pop()
		ax.bar(ind[i], data['y_vals'][i], width, color=color, alpha=0.65, edgecolor=color)

	ax.set_xticks(ind)
	xtickNames = plt.setp(ax, xticklabels=data['labels'])
	plt.setp(xtickNames, rotation=65)
	
	plt.savefig('data/' + my.DATA_FOLDER + 'plots/' + 'bar_' + data['name'].replace(' ','') + '.png')
