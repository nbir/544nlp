# -*- coding: utf-8 -*-

# Named Entity Recognizer - 544 NLP Assignment1
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE


##########~--------------------------------------~##########
##########~     SETTINGS - MAKE CHANGES HERE     ~##########
##########~--------------------------------------~##########

# FILES & FOLDERS
# Training data
TRAIN_DATA_FOLDER = 'data/train/'
TRAIN_DATA_FILE = 'eng.train.txt'

# Developement data
DEV_DATA_FOLDER = 'data/dev/'
DEV_DATA_FILE = 'eng.development.txt'

# Test data
TEST_DATA_FOLDER = 'data/test/'
TEST_DATA_FILE = 'eng.testing'

# Output
OUTPUT_FOLDER = 'data/out/'
OUTPUT_FILE = 'eng.testingdata.txt'
OUTPUT_FILE3 = 'eng.testingdata3.txt'


# Paths
WEKA_JAR_PATH = 'lib/'
PERL_EVAL_PATH = 'lib/'
PERL_EVAL_SCRIPT = 'eval.txt'

##########~--------------------------------------------------~##########
##########~     DO NOT CHANGE SETTINGS BEYOND THIS POINT     ~##########
##########~--------------------------------------------------~##########

# Files & folders
# arff files
# Train
TRAIN_DATA_FILE_ARFF_NEI = 'train_nei.arff'
TRAIN_DATA_FILE_ARFF_NEI_TAG = 'train_nei_tag.arff'
TRAIN_DATA_FILE_ARFF_NEC = 'train_nec.arff'
TRAIN_DATA_FILE_ARFF_NEC_TAG = 'train_nec_tag.arff'
# Dev
DEV_DATA_FILE_ARFF = 'dev.arff'
# Test
TEST_DATA_FILE_ARFF_NEI = 'test_nei.arff'
TEST_DATA_FILE_ARFF_NEI_TAG = 'test_nei_tag.arff'
TEST_DATA_FILE_ARFF_NEC = 'test_nec.arff'
TEST_DATA_FILE_ARFF_NEC_TAG_KNN = 'test_nec_tag_IBk.arff'
TEST_DATA_FILE_ARFF_NEC_TAG_J48 = 'test_nec_tag_J48.arff'
TEST_DATA_FILE_ARFF_NEC_TAG_NB = 'test_nec_tag_NB.arff'
TEST_DATA_FILE_ARFF_NEC_TAG_BN = 'test_nec_tag_BN.arff'
TEST_DATA_FILE_ARFF_NEC_TAG_PERCEPTRON = 'test_nec_tag_Perceptron.arff'
TEST_DATA_FILE_ARFF_NEC_TAG = 'test_nec_tag_combined.arff'	# combined
TEST_DATA_FILE_ARFF_NEC_TAG3 = 'test_nec_tag_combined3.arff'	# combined
# Eval
EVAL_PERL_FILE = 'eval_input'
EVAL_PERL_FILE3 = 'eval_input3'

# Model files
MODEL_FODLER = 'models/'
NEI_MODEL_FILE = 'nei_IBk.model'
NEC_MODEL_KNN_FILE = 'nec_IBk.model'
NEC_MODEL_J48_FILE = 'nec_J48.model'
NEC_MODEL_NB_FILE = 'nec_NB.model'
NEC_MODEL_BN_FILE = 'nec_BN.model'
NEC_MODEL_PERCEPTRON_FILE = 'nec_perceptron.model'


# Classifier names
CLASSIFIER_KNN = 'weka.classifiers.lazy.IBk -K 3 -x 4'
CLASSIFIER_J48 = 'weka.classifiers.trees.J48 -x 4'
CLASSIFIER_NB = 'weka.classifiers.bayes.NaiveBayes -x 4'
CLASSIFIER_BN = 'weka.classifiers.bayes.BayesNet -x 4'
CLASSIFIER_PERCEPTRON = 'weka.classifiers.functions.MultilayerPerceptron -x 4'


# Class labels/mappings
# BIO mapping
CLASS_MAPPING_BIO = {'B-PER':'B-PER', 'I-PER':'I-PER', 'B-LOC':'B-LOC', 'I-LOC':'I-LOC', 'B-ORG':'B-ORG', 'I-ORG':'I-ORG', 'B-MISC':'B-MISC', 'I-MISC':'I-MISC', 'O':'O'}
LABEL_STR_BIO = '{B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, B-MISC, I-MISC, O}'
# Unknown mapping
CLASS_MAPPING_UNKNOWN = {'B-PER':'?', 'I-PER':'?', 'B-LOC':'?', 'I-LOC':'?', 'B-ORG':'?', 'I-ORG':'?', 'B-MISC':'?', 'I-MISC':'?', 'O':'?'}
# 2 class named ent identification
CLASS_MAPPING_NEI = {'B-PER':'1', 'I-PER':'1', 'B-LOC':'1', 'I-LOC':'1', 'B-ORG':'1', 'I-ORG':'1', 'B-MISC':'1', 'I-MISC':'1', 'O':'0'}


# Gazetteer files (raw)
GAZ_PER_FNAME_RAW_FILE = 'CSV_Database_of_First_Names.csv'
GAZ_PER_LNAME_RAW_FILE = 'surnames.csv'
GAZ_LOC_RAW_FILE = 'dataen.txt'
# Gazetteer files (raw)
GAZ_FOLDER = 'data/gazetteer/'
GAZ_PER_FNAME_FILE = 'gazetteer_per_fname.txt'
GAZ_PER_LNAME_FILE = 'gazetteer_per_lname.txt'
GAZ_LOC_FILE = 'gazetteer_loc.txt'


# Linguistic
POS_PROPER_NOUN_LIST = ['NNP', 'NNPS']
POS_OTHER_NOUN_LIST = []
POS_DETERMINER_LIST = ['DT']
POS_VERB_LIST = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

# Trigger lists
# http://en.wikipedia.org/wiki/English_honorifics
# http://stylemanual.ngs.org/home/M/military-ranks
TRIGGER_LIST_PER_PREV = ['Mr.', 'Mr', 'Ms.', 'Ms', 'Miss.', 'Miss', 'Mrs.', 'Mrs', \
										'Sir', 'Madam', 'Madame', 'Lord', 'Lady', \
										'Dr.', 'Dr', 'Prof.', 'Prof', \
										'Sr.', 'Sr', 'Fr.', 'Fr', 'Rev.', 'Rev' \
										'Gen.', 'Gen', 'Lt.', 'Lt', 'Brig.', 'Brig', 'Col.', 'Col', 'Maj.', 'Maj', 'Capt.', 'Capt', 'Sgt.', 'Sgt', 'Cpl.', 'Cpl', 'Pvt.', 'Pvt', 'Pfc.', 'Pfc' \
										'Adm.', 'Adm', 'Cmdr.', 'Cmdr', 'Officer', 'Chief']

TRIGGER_LIST_ORG_PREV = ['of', 'from', 'for', 'the']
TRIGGER_LIST_ORG_NEXT = ['co.', 'co', 'corp.', 'corp', 'ltd.', 'ltd', 'pvt.', 'pvt', 'org.', 'org', 'inc.', 'inc']

TRIGGER_LIST_LOC_PREV = ['to', 'from', 'at', 'in']