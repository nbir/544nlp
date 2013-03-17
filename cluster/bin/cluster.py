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

import anyjson
import xml.etree.ElementTree as ET
import numpy as np
import pylab as pl

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import cluster
from sklearn.metrics import euclidean_distances
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler


def generate_clusters(name):
	# Generate feature matrix
	feature_types = ['bigram', 'noun_verb', 'stemmed', 'stemmed_pos', 'unigram', 'unigram_pos']
	#feature_types = ['unigram']
	mat_dir = 'data/' + my.DATA_FOLDER + '_feature_mat/' + name + '/'

	gold_file = 'data/' + my.DATA_FOLDER + 'gold/' + name + '.clust.xml'
	gold_tree = ET.parse(gold_file)
	gold_root = gold_tree.getroot()
	num_of_clusters = len([1 for c in gold_root.iter('entity')])
	
	for feature_type in feature_types:
		with open(mat_dir + feature_type, 'r') as fp1:
			feature_mat = anyjson.loads(fp1.read())
		tf_transformer = TfidfTransformer(use_idf=False).fit(feature_mat)
		X_train_tf = tf_transformer.transform(feature_mat)

		clustering = _cluster_k_means(X_train_tf, num_of_clusters)
		write_clustering_xml(name, 'kmeans__'+feature_type+'_tf', clustering)

		clustering = _cluster_dbscan(X_train_tf, num_of_clusters)
		write_clustering_xml(name, 'dbscan__'+feature_type+'_tf', clustering)

		clustering = _cluster_ward(X_train_tf, num_of_clusters)
		write_clustering_xml(name, 'ward__'+feature_type+'_tf', clustering)


		tfidf_transformer = TfidfTransformer()
		X_train_tfidf = tfidf_transformer.fit_transform(feature_mat)

		clustering = _cluster_k_means(X_train_tfidf, num_of_clusters)
		write_clustering_xml(name, 'kmeans__'+feature_type+'_tfidf', clustering)

		clustering = _cluster_dbscan(X_train_tfidf, num_of_clusters)
		write_clustering_xml(name, 'dbscan__'+feature_type+'_tfidf', clustering)

		clustering = _cluster_ward(X_train_tfidf, num_of_clusters)
		write_clustering_xml(name, 'ward__'+feature_type+'_tfidf', clustering)


def _cluster_k_means(feature_mat, k):
	km = cluster.KMeans(n_clusters=k)
	km.fit(feature_mat)
	labels = km.labels_

	#print labels
	clustering = dict([(c_id+1, []) for c_id in set(labels)])
	for i in range(0, len(labels)):
		clustering[labels[i]+1].append(i)
	return clustering

def _cluster_dbscan(feature_mat, k):
	dbscan = cluster.DBSCAN(eps=.2, min_samples=1)
	dbscan.fit(feature_mat.todense())
	labels = dbscan.labels_

	#print labels
	clustering = dict([(c_id+1, []) for c_id in set(labels)])
	for i in range(0, len(labels)):
		clustering[labels[i]+1].append(i)
	return clustering

def _cluster_ward(feature_mat, k):
	ward = cluster.Ward(n_clusters=k)
	ward.fit(feature_mat.toarray())
	labels = ward.labels_

	#print labels
	clustering = dict([(c_id+1, []) for c_id in set(labels)])
	for i in range(0, len(labels)):
		clustering[labels[i]+1].append(i)
	return clustering


def write_clustering_xml(name, feature_type, clustering):
	# Write back output of clustering to XML files
	tree = ET.Element('clustering', attrib={'name': name.replace('_', ' ')})
	for c_id in [c_id for c_id in clustering if c_id != 0]:
		en = ET.Element('entity', attrib={'id': str(c_id)})
		for doc_id in clustering[c_id]:
			doc = ET.Element('doc', attrib={'rank': str(doc_id)})
			en.append(doc)
		tree.append(en)

	if 0 in clustering:
		en = ET.Element('discarded')
		for doc_id in clustering[0]:
			doc = ET.Element('doc', attrib={'rank': str(doc_id)})
			en.append(doc)
		tree.append(en)

	out_dir = 'data/' + my.DATA_FOLDER + 'output/' + feature_type + '/'
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_dir + name + '.clust.xml', 'w') as fp1:
		fp1.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + ET.tostring(tree))
