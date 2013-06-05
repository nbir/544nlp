# -*- coding: utf-8 -*-

# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE
#
#

import csv
import numpy

from sklearn import svm
from sklearn import preprocessing
from sklearn import decomposition
from sklearn.lda import LDA


class Data:
#	feats 	list of feature names
#	X 			feature matrix ndarray
#	y 			vector of class labels

#def __init__(self, n):	

# SET functions
	def set_X(self, X):
		self.X = numpy.array(X)
	def set_y(self, y):
		self.y = numpy.array(y)

# LOAD functions
	def load_X(self, path):
		feat_mat = []
		with open(path, 'rb') as fp_x:
			cr = csv.reader(fp_x, delimiter=',')
			self.feats = cr.next()
			for row in cr:
				row = [float(val) for val in row]
				feat_mat.append(row)
		self.set_X(feat_mat)
		#self.X = feat_mat
		#print self.X
	def load_y(self, path):
		labels = []
		with open(path, 'rb') as fp_x:
			cr = csv.reader(fp_x, delimiter=',')
			_ = cr.next()
			for row in cr:
				labels.append(int(row[0]))
		self.set_y(labels)
		#self.y = labels
		#print self.y
	def load_Xy(self, path_x, path_y):
		self.load_X(path_x)
		self.load_y(path_y)


# GET functions
	def get_X(self):
		return self.X.tolist()
	def get_feats(self):
		return self.feats
	def get_y(self):
		return self.y.tolist()

# SAVE functions
	def save_X(self, path):
		X = self.get_X()
		with open(path, 'wb') as fp_x:
			cw = csv.writer(fp_x, delimiter=',')
			for row in X:
				cw.writerow(row)
	def save_y(self, path):
		y = self.get_y()
		with open(path, 'wb') as fp_y:
			cw = csv.writer(fp_y, delimiter=',')
			for val in y:
				cw.writerow([val])


# ALTER functions
	def reorder(self):
		# DO NOT USE / NOT REQUIRED
		X = self.get_X()
		y = self.get_y()
		Xnew = []
		ynew = []
		mid = len(y)/2
		for i in range(0, mid):
			Xnew.extend([X[i], X[mid+i]])
			ynew.extend([y[i], y[mid+i]])
		self.set_X(Xnew)
		self.set_y(ynew)
	def extend_X(self, new):
		X = self.get_X()
		newX = new.get_X()
		self.feats += new.get_feats()
		for i in range(0, len(X)):
			X[i].extend(newX[i])
		self.set_X(X)
	def remove_feat(self, ind):
		if isinstance(ind, str):
			ind = self.feats.index(ind)
		X = self.get_X()
		self.feats.pop(ind)
		for i in range(0, len(X)):
			X[i].pop(ind)
		self.set_X(X)


# NORMALIZE functions
	def norm_feat(self):
		#if isinstance(ind, str):
		#	ind = self.feats.index(ind)
		self.X = preprocessing.normalize(self.X, norm='l2', axis=1, copy=True)
	def scale_feats(self):
		self.X = preprocessing.scale(self.X)

# FEATURE REDUCTION
	def reduce_pca(self):
		_, before = self.X.shape
		pca = decomposition.PCA()
		pca.fit(self.X)
		#print sorted(pca.explained_variance_ratio_.tolist())
		#print len(pca.explained_variance_ratio_), sum(pca.explained_variance_ratio_)
		for i in range(0, len(pca.explained_variance_ratio_)):
			if sum(pca.explained_variance_ratio_[0:i]) > 0.9:
				break;
		pca = decomposition.PCA(n_components=i)
		self.X = pca.fit(self.X).transform(self.X)
		_, after = self.X.shape
		#print 'Reduced from %s to %s components' % (before, after)





# PRINT functions
	def show_shape(self):
		print self.X.shape
	def show_Xlen(self):
		lens = []
		for i in range(0, len(self.X)):
			lens.append(len(self.X[i]))
		print 'Length of rows: ', sent(lens)
	def show_feat(self, ind):
		if isinstance(ind, str):
			ind = self.feats.index(ind)
		fval = []
		for i in range(0, len(self.X)):
			print self.X[i][ind]
			fval.append(self.X[i][ind])
		print 'SUM = %s, MEAN = %s, MIN = %s, MAX = %s' % (sum(fval), sum(fval)/len(fval), min(fval), max(fval))
	def show_y(self):
		for i in range(0, len(self.y)):
			print self.y[i]
