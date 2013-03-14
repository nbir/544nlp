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

import csv
import re

def build_gazetteer_per():
	# firstname list
	fp1 = open(my.GAZ_FOLDER + my.GAZ_PER_FNAME_RAW_FILE, 'rU')
	csv_reader = csv.reader(fp1)
	dump = csv_reader.next()
	fp2 = open(my.GAZ_FOLDER + my.GAZ_PER_FNAME_FILE, 'wb')
	csv_writer = csv.writer(fp2)
	for row in csv_reader:
		csv_writer.writerow([row[0].strip()])

	# lastname list
	fp1 = open(my.GAZ_FOLDER + my.GAZ_PER_LNAME_RAW_FILE, 'rb')
	csv_reader = csv.reader(fp1, delimiter=',')
	dump = csv_reader.next()
	fp2 = open(my.GAZ_FOLDER + my.GAZ_PER_LNAME_FILE, 'wb')
	csv_writer = csv.writer(fp2)
	for row in csv_reader:
		csv_writer.writerow([row[0].strip().capitalize()])

def build_gazetteer_loc():
	# location list
	fp1 = open(my.GAZ_FOLDER + my.GAZ_LOC_RAW_FILE, 'rU')
	csv_reader = csv.reader(fp1, dialect=csv.excel_tab)
	dump = csv_reader.next()
	fp2 = open(my.GAZ_FOLDER + my.GAZ_LOC_FILE, 'wb')
	csv_writer = csv.writer(fp2)
	for row in csv_reader:
		words = re.split('\s+', row[1].strip())
		for word in words:
			if(len(word) > 0):
				csv_writer.writerow([word])