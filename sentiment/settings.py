# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import numpy


##########~--------------------------------------~##########
##########~     SETTINGS - MAKE CHANGES HERE     ~##########
##########~--------------------------------------~##########

# FILES & FOLDERS
#DATA_FOLDER = 'amida/'
DATA_FOLDER = 'youtube/'


# PRAAT o/p file name formats
PFF_amida = '%s.Mix-Headset.wav.csv'
PFF_youtube = '%s.csv'
PRAAT_FILE_FORMAT = PFF_amida if DATA_FOLDER == 'amida/' else PFF_youtube


##########~--------------------------------------------------~##########
##########~     DO NOT CHANGE SETTINGS BEYOND THIS POINT     ~##########
##########~--------------------------------------------------~##########

# Minimum word count to include unigram in feature space
MIN_WORD_COUNT = 3
MIN_CWORD_COUNT = 5

# Subjectivity types for the two classes
CLASS_1 = ['2.2']		# Positive Subjective
CLASS_2 = ['2.1']		# Negative Subjective

# Feature type code to filename mapping
FEAT_TYPE_MAP = {
	'T' : 'X_unigram.csv',
	'C' : 'X_charngram.csv',
	'S' : 'X_sentiwordnet.csv',
	'A' : 'X_audio.csv'
	}

# SVAM parameter space
SVM_KERNAL_SPACE = ['linear', 'poly', 'rbf']
#SVM_KERNAL_SPACE = ['linear', 'rbf']
#SVM_C_SPACE = numpy.logspace(-3, 3, 10)
SVM_C_SPACE = numpy.logspace(-1, 1, 10)