# -*- coding: utf-8 -*-

# Named Entity Recognizer - 544 NLP Assignment1
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE


import sys
import os
sys.path.insert(0, os.path.abspath('..'))

import settings as my
import feature_generator as feat

import csv
from lib import arff


def generate_features_for_nei(dir, in_file, out_arff, mapping=None, label_str=None):
# 
# 
#
	# load gazetteers
	gaz_fname = load_gaz(my.GAZ_PER_FNAME_FILE)
	gaz_lname = load_gaz(my.GAZ_PER_LNAME_FILE)
	gaz_loc = load_gaz(my.GAZ_LOC_FILE)

	# Write 
	with open(dir + out_arff, 'wb') as fp2:
		fp2.write('@relation nei' + '\n\n')

		fp2.write('@attribute position integer' + '\n')
		fp2.write('@attribute is_p_noun {0, 1}' + '\n')
		fp2.write('@attribute is_symbol {0, 1}' + '\n')
		fp2.write('@attribute next_word_verb {0, 1}' + '\n')

		fp2.write('@attribute init_cap {0, 1}' + '\n')
		fp2.write('@attribute all_cap {0, 1}' + '\n')
		fp2.write('@attribute prev_word_cap {0, 1}' + '\n')
		fp2.write('@attribute next_word_cap {0, 1}' + '\n')

		fp2.write('@attribute in_gaz_per_fname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_per_lname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_loc {0, 1}' + '\n')

		# fp2.write('@attribute class {B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, B-MISC, I-MISC, O}' + '\n\n')
		if label_str:
			fp2.write('@attribute class ' + label_str + '\n\n')
		else:
			fp2.write('@attribute class {0, 1}' + '\n\n')
		
		fp2.write('@data' + '\n\n')

	fp2 = open(dir + out_arff, 'ab')
	csv_writer = csv.writer(fp2, delimiter=',')

	with open(dir + in_file, 'rb') as fp1:
		csv_reader = csv.reader(fp1, delimiter=' ', quoting=csv.QUOTE_NONE)
		sentence = []

		print 'Reading file..'
		row_count = 0
		for row in csv_reader:
			row_count += 1
			print row_count

			if len(row) == 0 or (row[0].strip() == ''):	# process sentence
			#if(row[0].strip() == ''):	# process sentence
				sentence_len = len(sentence)

				for word_position in range(0, sentence_len):
				#for token in sentence:
					token = sentence[word_position]
					feature_vector = []

					feature_vector.append(feat.position(sentence_len, word_position))	# position
					feature_vector.append(feat.is_p_noun(token))	# is_p_noun
					feature_vector.append(feat.is_symbol(token))	# is_symbol
					feature_vector.append(feat.next_word_verb(sentence, word_position))	# next_word_verb
					
					feature_vector.append(feat.init_cap(token))	# init_cap
					feature_vector.append(feat.all_cap(token))	# all_cap
					feature_vector.append(feat.prev_word_cap(sentence, word_position))	# prev_word_cap
					feature_vector.append(feat.next_word_cap(sentence, word_position))	# next_word_cap

					feature_vector.append(feat.in_gaz(token, gaz_fname)) # in_gaz_per_fname
					feature_vector.append(feat.in_gaz(token, gaz_lname)) # in_gaz_per_lname
					feature_vector.append(feat.in_gaz(token, gaz_loc)) # in_gaz_loc

					feature_vector.append('?' if not mapping else mapping[token[2]]) # class
					
					csv_writer.writerow(feature_vector)

				sentence = []
			else:
				sentence.append(row)
		print 'Read ' + str(row_count) + ' rows in file.'
		fp2.close()

def load_gaz(filename):
	gaz_list = []
	with open(my.GAZ_FOLDER + filename, 'rb') as fp:
		gaz_list = [word.strip() for word in fp.readlines()]
	return gaz_list


def build_model_nei(classifier, model_name, verbose=True):
#
#
	os.system('java -Xmx2048m -cp ' + my.WEKA_JAR_PATH + 'weka.jar ' + \
		classifier + ' ' + \
		'-t ' + my.TRAIN_DATA_FOLDER + my.TRAIN_DATA_FILE_ARFF_NEI + ' ' + \
		'-d ' + my.MODEL_FODLER + model_name + ' ' + \
		('-v' if verbose else ' '))


def classification_nei(model_file, dir, in_arff, out_arff):
#
#
	os.system('java -Xmx2048m -cp ' + my.WEKA_JAR_PATH + 'weka.jar ' + \
		'weka.filters.supervised.attribute.AddClassification ' + \
		'-serialized ' + my.MODEL_FODLER + model_file + ' ' + \
		'-classification ' + \
		'-remove-old-class ' + \
		'-i ' + dir + in_arff + ' ' + \
		'-o ' + dir + out_arff + ' ' + \
		'-c last')


def generate_features_for_nec(dir, in_file, in_arff, out_arff, mapping=None, label_str=None):
#
#
#
	# load input arff file
	in_arff = arff.load(open(dir + in_arff, 'rb'))
	iter_in_arff = iter(in_arff['data'])

	# append new features and write new arff file
	with open(dir + out_arff, 'wb') as fp2:
		fp2.write('@relation nec' + '\n\n')

		fp2.write('@attribute position integer' + '\n')
		fp2.write('@attribute is_p_noun {0, 1}' + '\n')
		fp2.write('@attribute is_symbol {0, 1}' + '\n')
		fp2.write('@attribute next_word_verb {0, 1}' + '\n')

		fp2.write('@attribute init_cap {0, 1}' + '\n')
		fp2.write('@attribute all_cap {0, 1}' + '\n')
		fp2.write('@attribute prev_word_cap {0, 1}' + '\n')
		fp2.write('@attribute next_word_cap {0, 1}' + '\n')

		fp2.write('@attribute in_gaz_per_fname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_per_lname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_loc {0, 1}' + '\n')

		fp2.write('@attribute is_ne {0, 1}' + '\n')		# input feature vector ends here
		fp2.write('@attribute is_prev_ne {-1, 0, 1}' + '\n')
		fp2.write('@attribute is_next_ne {-1, 0, 1}' + '\n')

		fp2.write('@attribute length integer' + '\n')

		fp2.write('@attribute prev_trigger_per {0, 1}' + '\n')
		fp2.write('@attribute prev_trigger_org {0, 1}' + '\n')
		fp2.write('@attribute next_trigger_org {0, 1}' + '\n')
		fp2.write('@attribute prev_trigger_loc {0, 1}' + '\n')

		if label_str:
			fp2.write('@attribute class ' + label_str + '\n\n')
		else:
			fp2.write('@attribute class {0, 1}' + '\n\n')
		
		fp2.write('@data' + '\n\n')

	fp2 = open(dir + out_arff, 'ab')
	csv_writer = csv.writer(fp2, delimiter=',')

	with open(dir + in_file, 'rb') as fp1:
		csv_reader = csv.reader(fp1, delimiter=' ', quoting=csv.QUOTE_NONE)
		sentence = []
		sentence_feat_vec = []

		print 'Reading file.. and appending new features...`'
		row_count = 0
		for row in csv_reader:
			row_count += 1
			#print row_count

			if len(row) == 0 or (row[0].strip() == ''):	# process sentence
			#if(row[0].strip() == ''):	# process sentence
				sentence_len = len(sentence)

				for word_position in range(0, sentence_len):
				#for token in sentence:
					token = sentence[word_position]
					#feature_vector = []
					feature_vector = sentence_feat_vec[word_position]
					feature_vector[0] = int(feature_vector[0])

					#feature_vector.append(feat.position(sentence_len, word_position))	# position
					#feature_vector.append(feat.is_p_noun(token))	# is_p_noun
					#feature_vector.append(feat.is_symbol(token))	# is_symbol
					#feature_vector.append(feat.next_word_verb(sentence, word_position))	# next_word_verb
					
					#feature_vector.append(feat.init_cap(token))	# init_cap
					#feature_vector.append(feat.all_cap(token))	# all_cap
					#feature_vector.append(feat.prev_word_cap(sentence, word_position))	# prev_word_cap
					#feature_vector.append(feat.next_word_cap(sentence, word_position))	# next_word_cap

					#feature_vector.append(feat.in_gaz(token, gaz_fname)) # in_gaz_per_fname
					#feature_vector.append(feat.in_gaz(token, gaz_lname)) # in_gaz_per_lname
					#feature_vector.append(feat.in_gaz(token, gaz_loc)) # in_gaz_loc

					# is_ne
					feature_vector.append(feat.is_prev_ne(sentence_feat_vec, word_position))	# is_prev_ne
					feature_vector.append(feat.is_next_ne(sentence_feat_vec, word_position))	# is_next_ne

					feature_vector.append(feat.length(token))	# length
					

					feature_vector.append(feat.prev_trigger_per(sentence, word_position))	# prev_trigger_per
					feature_vector.append(feat.prev_trigger_org(sentence, word_position))	# prev_trigger_org
					feature_vector.append(feat.next_trigger_org(sentence, word_position))	# next_trigger_org
					feature_vector.append(feat.prev_trigger_loc(sentence, word_position))	# prev_trigger_loc

					feature_vector.append('?' if not mapping else mapping[token[2]]) # class
					
					csv_writer.writerow(feature_vector)

				sentence = []
				sentence_feat_vec = []
			else:
				sentence.append(row)
				sentence_feat_vec.append(iter_in_arff.next())

		print 'Read ' + str(row_count) + ' rows in file.'
		fp2.close()


def build_model_nec(classifier, model_name, verbose=True):
#
#
	os.system('java -Xmx2048m -cp ' + my.WEKA_JAR_PATH + 'weka.jar ' + \
		classifier + ' ' + \
		'-t ' + my.TRAIN_DATA_FOLDER + my.TRAIN_DATA_FILE_ARFF_NEC + ' ' + \
		'-d ' + my.MODEL_FODLER + model_name + ' ' + \
		('-v' if verbose else ' '))


def classification_nec(model_file, dir, in_arff, out_arff):
#
#
	os.system('java -Xmx2048m -cp ' + my.WEKA_JAR_PATH + 'weka.jar ' + \
		'weka.filters.supervised.attribute.AddClassification ' + \
		'-serialized ' + my.MODEL_FODLER + model_file + ' ' + \
		'-classification ' + \
		'-remove-old-class ' + \
		'-i ' + dir + in_arff + ' ' + \
		'-o ' + dir + out_arff + ' ' + \
		'-c last')


def generate_output_file(dir_in, in_file, dir_arff, in_arff, dir_out, out_file):
#
#
#
	# load input arff file
	in_arff = arff.load(open(dir_arff + in_arff, 'rb'))
	iter_in_arff = iter(in_arff['data'])

	fp2 = open(dir_out + out_file, 'wb')
	csv_writer = csv.writer(fp2, delimiter=' ', lineterminator='\n')

	with open(dir_in + in_file, 'rb') as fp1:
		csv_reader = csv.reader(fp1, delimiter=' ', quoting=csv.QUOTE_NONE)
		
		row_count = 0
		for row in csv_reader:
			row_count += 1
			#print row_count

			if len(row) == 0 or (row[0].strip() == ''):	# process sentence
			#if(row[0].strip() == ''):	# write blank
				csv_writer.writerow([])
				#csv_writer.writerow(['', ''])
			else:
				feature_vector = iter_in_arff.next()
				csv_writer.writerow([feature_vector[-1:][0]])
				#csv_writer.writerow([row[0].strip(), feature_vector[-1:][0]])

		print 'Written ' + str(row_count) + ' lines to output file.'
		fp2.close()


def combine_output(dir_arff, in_arff_list, dir_out, out_arff, override, label_str=None):
#
#
#
	# load input arff file
	in_arff = {}
	iter_in_arff = {}
	for arff_name in in_arff_list:
		in_arff[arff_name] = arff.load(open(dir_arff + arff_name, 'rb'))
		iter_in_arff[arff_name] = iter(in_arff[arff_name]['data'])

	with open(dir_out + out_arff, 'wb') as fp2:
		fp2.write('@relation ner' + '\n\n')

		fp2.write('@attribute position integer' + '\n')
		fp2.write('@attribute is_p_noun {0, 1}' + '\n')
		fp2.write('@attribute is_symbol {0, 1}' + '\n')
		fp2.write('@attribute next_word_verb {0, 1}' + '\n')

		fp2.write('@attribute init_cap {0, 1}' + '\n')
		fp2.write('@attribute all_cap {0, 1}' + '\n')
		fp2.write('@attribute prev_word_cap {0, 1}' + '\n')
		fp2.write('@attribute next_word_cap {0, 1}' + '\n')

		fp2.write('@attribute in_gaz_per_fname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_per_lname {0, 1}' + '\n')
		fp2.write('@attribute in_gaz_loc {0, 1}' + '\n')

		fp2.write('@attribute is_ne {0, 1}' + '\n')		# input feature vector ends here
		fp2.write('@attribute is_prev_ne {-1, 0, 1}' + '\n')
		fp2.write('@attribute is_next_ne {-1, 0, 1}' + '\n')

		fp2.write('@attribute length integer' + '\n')

		fp2.write('@attribute prev_trigger_per {0, 1}' + '\n')
		fp2.write('@attribute prev_trigger_org {0, 1}' + '\n')
		fp2.write('@attribute next_trigger_org {0, 1}' + '\n')
		fp2.write('@attribute prev_trigger_loc {0, 1}' + '\n')

		if label_str:
			fp2.write('@attribute class ' + label_str + '\n\n')
		else:
			fp2.write('@attribute class {0, 1}' + '\n\n')
		
		fp2.write('@data' + '\n\n')

	fp2 = open(dir_out + out_arff, 'ab')
	csv_writer = csv.writer(fp2, delimiter=',')

	row_count = 0
	for i in range(0, len(in_arff[override]['data'])):
		predict_list = []
		feature_vector = {}
		for arff_name in in_arff_list:
			feature_vector[arff_name] = iter_in_arff[arff_name].next()
			predict_list.append(feature_vector[arff_name][-1:][0])

		out_feat_vector = list(feature_vector[override])
		for j in range(0, len(out_feat_vector)-1):
			out_feat_vector[j] = int(out_feat_vector[j])
		if len(predict_list) != len(set(predict_list)): # if all precitions are unique, use override
			out_feat_vector[-1] = max(set(predict_list), key=predict_list.count)

		#print predict_list
		#print out_feat_vector[-1:][0]

		row_count += 1
		csv_writer.writerow(out_feat_vector)

	print 'Written ' + str(row_count) + ' lines to output file.'
	fp2.close()


