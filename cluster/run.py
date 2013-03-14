# -*- coding: utf-8 -*-

# Named Entity Recognizer - 544 NLP Assignment1
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import sys
import settings as my

import bin.prep
import bin.testtrain as tt
import bin.eval


##########~-------------------------------------------------~##########
##########~     NON-EXPERIMENT/PREPROCESSING DIRECTIVES     ~##########
##########~-------------------------------------------------~##########

if '-prep' in sys.argv:
	print	'----------     BUILDING GAZETTEER LISTS     ----------'
	bin.prep.build_gazetteer_per()
	bin.prep.build_gazetteer_loc()

##########~---------------------------------------------------~##########
##########~     EXPERIMENT/CLASSIFICATION TASK DIRECTIVES     ~##########
##########~---------------------------------------------------~##########
# Train model
if '-train' in sys.argv:
	print	'----------     TRAINING     ----------'
	print 'Building feature set for Named Entity Identification task...'
	#tt.generate_features_for_nei(my.TRAIN_DATA_FOLDER, my.TRAIN_DATA_FILE, my.TRAIN_DATA_FILE_ARFF_NEI, my.CLASS_MAPPING_NEI)
	print 'Training model for Named Entity Identification task...'
	#tt.build_model_nei(my.CLASSIFIER_KNN, my.NEI_MODEL_FILE)
	print 'Building feature set for Named Entity Classification task...'
	#tt.generate_features_for_nec(my.TRAIN_DATA_FOLDER, my.TRAIN_DATA_FILE, my.TRAIN_DATA_FILE_ARFF_NEI, my.TRAIN_DATA_FILE_ARFF_NEC, my.CLASS_MAPPING_BIO, my.LABEL_STR_BIO)
	print 'Training model for Named Entity Classification task...'
	#tt.build_model_nec(my.CLASSIFIER_KNN, my.NEC_MODEL_KNN_FILE)
	#tt.build_model_nec(my.CLASSIFIER_J48, my.NEC_MODEL_J48_FILE)
	#tt.build_model_nec(my.CLASSIFIER_NB, my.NEC_MODEL_NB_FILE)
	#tt.build_model_nec(my.CLASSIFIER_BN, my.NEC_MODEL_BN_FILE)
	#tt.build_model_nec(my.CLASSIFIER_PERCEPTRON, my.NEC_MODEL_PERCEPTRON_FILE)
	print 'Done!'

# Test model
if '-test' in sys.argv:
	print	'----------     TEST     ----------'
	print 'Building feature set for Named Entity Identification task...'
	#tt.generate_features_for_nei(my.TEST_DATA_FOLDER, my.TEST_DATA_FILE, my.TEST_DATA_FILE_ARFF_NEI)
	print 'Classification... Named Entity Identification task...'
	#tt.classification_nei(my.NEI_MODEL_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEI, my.TEST_DATA_FILE_ARFF_NEI_TAG)
	print 'Building feature set for Named Entity Classification task...'

	#tt.generate_features_for_nec(my.TEST_DATA_FOLDER, my.TEST_DATA_FILE, my.TEST_DATA_FILE_ARFF_NEI_TAG, my.TEST_DATA_FILE_ARFF_NEC, None, my.LABEL_STR_BIO)
	print 'Classification... Named Entity Classification task...'
	print 'IBk.'
	#tt.classification_nec(my.NEC_MODEL_KNN_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC, my.TEST_DATA_FILE_ARFF_NEC_TAG_KNN)
	print 'J48.'
	#tt.classification_nec(my.NEC_MODEL_J48_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC, my.TEST_DATA_FILE_ARFF_NEC_TAG_J48)
	print 'NaiveBayes.'
	#tt.classification_nec(my.NEC_MODEL_NB_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC, my.TEST_DATA_FILE_ARFF_NEC_TAG_NB)
	print 'BayesNet.'
	#tt.classification_nec(my.NEC_MODEL_BN_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC, my.TEST_DATA_FILE_ARFF_NEC_TAG_BN)
	print 'MultilayerPerceptron.'
	#tt.classification_nec(my.NEC_MODEL_PERCEPTRON_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC, my.TEST_DATA_FILE_ARFF_NEC_TAG_PERCEPTRON)
	
	print 'Combining output of multiple classifiers...'
	#tt.combine_output(my.TEST_DATA_FOLDER, [my.TEST_DATA_FILE_ARFF_NEC_TAG_KNN, my.TEST_DATA_FILE_ARFF_NEC_TAG_J48, my.TEST_DATA_FILE_ARFF_NEC_TAG_NB, my.TEST_DATA_FILE_ARFF_NEC_TAG_BN, my.TEST_DATA_FILE_ARFF_NEC_TAG_PERCEPTRON], my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC_TAG, my.TEST_DATA_FILE_ARFF_NEC_TAG_J48, my.LABEL_STR_BIO)
	#tt.combine_output(my.TEST_DATA_FOLDER, [my.TEST_DATA_FILE_ARFF_NEC_TAG_KNN, my.TEST_DATA_FILE_ARFF_NEC_TAG_J48, my.TEST_DATA_FILE_ARFF_NEC_TAG_PERCEPTRON], my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC_TAG3, my.TEST_DATA_FILE_ARFF_NEC_TAG_J48, my.LABEL_STR_BIO)
	print 'Generating output file...'
	tt.generate_output_file(my.TEST_DATA_FOLDER, my.TEST_DATA_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC_TAG, my.OUTPUT_FOLDER, my.OUTPUT_FILE)
	tt.generate_output_file(my.TEST_DATA_FOLDER, my.TEST_DATA_FILE, my.TEST_DATA_FOLDER, my.TEST_DATA_FILE_ARFF_NEC_TAG3, my.OUTPUT_FOLDER, my.OUTPUT_FILE3)
	print 'Done!'


# Single classifier
if '-single' in sys.argv:
	# generate output text
	#tt.generate_output_file(my.TEST_DATA_FOLDER, my.TEST_DATA_FILE, my.TEST_DATA_FOLDER, 'test_nec_tag_J48_laplace.arff', my.OUTPUT_FOLDER, 'only_J48_laplace.txt')

	# eval
	#bin.eval.generate_eval_file(my.DEV_DATA_FOLDER, my.DEV_DATA_FILE, my.OUTPUT_FOLDER, 'only_J48_laplace.txt', my.OUTPUT_FOLDER, 'only_J48_laplace')
	#bin.eval.count_corect_predictions(my.OUTPUT_FOLDER, 'only_J48_laplace')
	#bin.eval.run_eval_script(my.OUTPUT_FOLDER, 'only_J48_laplace')	
	print 'Done!'
	

# Eval output
if '-eval' in sys.argv:
	print	'----------     EVAL     ----------'
	print 'Generating evaluation Data file for perl script...'
	print 'argMax on 5 classifier outputs:'
	bin.eval.generate_eval_file(my.DEV_DATA_FOLDER, my.DEV_DATA_FILE, my.OUTPUT_FOLDER, my.OUTPUT_FILE, my.OUTPUT_FOLDER, my.EVAL_PERL_FILE)
	bin.eval.count_corect_predictions(my.OUTPUT_FOLDER, my.EVAL_PERL_FILE)
	bin.eval.run_eval_script(my.OUTPUT_FOLDER, my.EVAL_PERL_FILE)

	print '\nargMax on 3 classifier outputs:'
	bin.eval.generate_eval_file(my.DEV_DATA_FOLDER, my.DEV_DATA_FILE, my.OUTPUT_FOLDER, my.OUTPUT_FILE3, my.OUTPUT_FOLDER, my.EVAL_PERL_FILE3)
	bin.eval.count_corect_predictions(my.OUTPUT_FOLDER, my.EVAL_PERL_FILE3)
	bin.eval.run_eval_script(my.OUTPUT_FOLDER, my.EVAL_PERL_FILE3)
	print 'Done!'



