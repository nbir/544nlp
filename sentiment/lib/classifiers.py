# -*- coding: utf-8 -*-

# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE
#
#

import settings as my

import csv
import numpy
from pprint import pprint
import matplotlib.pyplot as plt
import pylab as pl


from sklearn import svm
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn import tree
from sklearn import ensemble


class ClassifySVM:
#	Xy					Data object with X & y
#	train_ind		Training indices
#	test_ind		Test indices
# kernel 			Best kernel parameter value
# C 					Bese C parameter value
# scores = {'kernel1':
#								'c_val1': <float> ...}
# train_acc 	Training accuracy
# test_acc 		Testing accuracy

	def __init__(self, data):
		self.Xy = data
		self.scores = {}
		self._split_train_test()
	def _split_train_test(self):
		folds = cross_validation.StratifiedKFold(self.Xy.y, 4)
		for self.train_ind, self.test_ind in folds:
			break

# Call this
	def learn(self):
		self.learn_param()
		self.choose_best_param()
		self.find_test_acc()
		self.show_scores()

# Training
	def learn_param(self):
		train_X, train_y = self.Xy.X[self.train_ind], self.Xy.y[self.train_ind]
		#test_X, test_y = self.Xy.X[self.test_ind], self.Xy.y[self.test_ind]

		#kernel_space = ['linear', 'poly', 'rbf']
		#c_space = numpy.logspace(-10, 0, 10)
		kernel_space = my.SVM_KERNAL_SPACE
		c_space = my.SVM_C_SPACE

		for k in kernel_space:
			self.scores[k] = {}
			for c in c_space:
				#print 'Now training for k=%s, c=%s' % (k, c)
				cv = cross_validation.StratifiedKFold(train_y, 10)
				svc = svm.SVC(C=c, kernel=k)
				scores = cross_validation.cross_val_score(svc, train_X, train_y, cv=cv, n_jobs=-1)
				#self.scores[k][c] = max(scores.tolist())		#	choose max acc of CV
				self.scores[k][c] = scores.mean()						#	choose mean acc of CV
				#print max(scores.tolist()), scores.mean()
	def choose_best_param(self):
		max_score, max_k, max_c = 0.0, '', 0.0
		for k in self.scores:
			for c in self.scores[k]:
				if self.scores[k][c] > max_score:
					max_score, max_k, max_c = self.scores[k][c], k, c
		self.train_acc, self.kernel, self.C = round(max_score, 4), k, c

# Testing
	def find_test_acc(self):
		train_X, train_y = self.Xy.X[self.train_ind], self.Xy.y[self.train_ind]
		test_X, test_y = self.Xy.X[self.test_ind], self.Xy.y[self.test_ind]

		svc = svm.SVC(C=self.C, kernel=self.kernel)
		svc.fit(train_X, train_y)
		self.test_acc = round(svc.score(test_X, test_y), 4)
	def show_scores(self):
		print 'TRAIN, TEST = %8s, %8s' % (self.train_acc, self.test_acc)
# Get
	def get_train_ind(self):
		return self.train_ind
	def get_test_ind(self):
		return self.test_ind
	def get_train_acc(self):
		return self.train_acc
	def get_test_acc(self):
		return self.test_acc

# Plot
	def plot_train(self, path):
		fig = plt.figure(figsize=(8,5))
		ax = fig.add_subplot(111)
		ax.set_autoscaley_on(False)
		ax.set_ylim([0,1])
		plt.subplots_adjust(left=0.075, right=0.99, top=0.98, bottom=0.105)
		ax.set_ylabel('Training accuracy')
		ax.set_xlabel('C')

		#c_space = numpy.logspace(-10, 0, 10)
		c_space = my.SVM_C_SPACE
		lines = {}

		for k in self.scores:
			lines[k] = [self.scores[k][c] for c in self.scores[k]]
			lines[k] = ax.semilogx(c_space, lines[k])

		ax.legend(tuple(lines[k][0] for k in lines), tuple([k for k in lines]), fontsize=11)
		plt.savefig(path)


################################################################################

class ClassifyDT:
#	Xy					Data object with X & y
# train_acc 	Training accuracy

	def __init__(self, data):
		self.Xy = data

# Call this
	def learn(self):
		self.find_best_acc()
		self.show_scores()

# Cross validation
	def find_best_acc(self):
		cv = cross_validation.StratifiedKFold(self.Xy.y, 10)
		dt = tree.DecisionTreeClassifier()
		scores = cross_validation.cross_val_score(dt, self.Xy.X, self.Xy.y, cv=cv, n_jobs=-1)
		self.train_acc = round(scores.max(), 4)
	def show_scores(self):
		print 'TRAIN = %8s' % self.train_acc
# Get
	def get_train_acc(self):
		return self.train_acc

################################################################################


class ClassifyRF:
#	Xy					Data object with X & y
# train_acc 	Training accuracy

	def __init__(self, data):
		self.Xy = data

# Call this
	def learn(self):
		self.find_best_acc()
		self.show_scores()

# Cross validation
	def find_best_acc(self):
		cv = cross_validation.StratifiedKFold(self.Xy.y, 10)
		rf = ensemble.RandomForestClassifier()
		scores = cross_validation.cross_val_score(rf, self.Xy.X, self.Xy.y, cv=cv, n_jobs=-1)
		self.train_acc = round(scores.max(), 4)
	def show_scores(self):
		print 'TRAIN = %8s' % self.train_acc
# Get
	def get_train_acc(self):
		return self.train_acc
