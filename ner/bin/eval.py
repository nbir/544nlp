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


def generate_eval_file(dir_file, in_file, dir_predict, predict_file, dir_out, out_file):
# 
# 
#
	fp2 = open(dir_predict + predict_file, 'rb')
	csv_reader2 = csv.reader(fp2, delimiter=' ', quoting=csv.QUOTE_NONE)

	fp3 = open(dir_out + out_file, 'w')
	#csv_writer = csv.writer(fp3, delimiter=' ', lineterminator='\n')
	#csv_writer = csv.writer(fp3, delimiter=' ')
	#out_str = ''

	with open(dir_file + in_file, 'rb') as fp1:
		csv_reader1 = csv.reader(fp1, delimiter=' ', quoting=csv.QUOTE_NONE)

		row_count = 0
		for row1 in csv_reader1:
			row_count += 1
			#print row_count
			row2 = csv_reader2.next()
			#if row1[0] != '' and row1[0] != '-DOCSTART-':
				#csv_writer.writerow([row1[0], row1[2], row2[1]])
			fp3.write(row1[0] + ' ' + row1[2] + ' ' + row2[1] + '\n')
			#else:
				#print row1
			#out_str += row1[0] + ' ' + row1[2] + ' ' + row2[1] + '\n'
		#fp3.write(out_str)
		print 'Written ' + str(row_count) + ' rows.'


def count_corect_predictions(dir, in_file):
#
#
	with open(dir + in_file, 'rb') as fp:
		csv_reader = csv.reader(fp, delimiter=' ', quoting=csv.QUOTE_NONE)

		others = 0
		_others = 0
		correct_others = 0
		correct__others = 0
		for row in csv_reader:
			if row[1] == 'O':
				others += 1
				if row[1] == row[2]:
					correct_others += 1
			else:
				_others += 1
			 	if row[1] == row[2]:
					correct__others += 1

		print 'File ' + in_file + ' has ' + str(correct__others) + ' correct predictions of ' + str(_others) + ' Named Entity tags tags.' 
		print 'File ' + in_file + ' has ' + str(correct_others) + ' correct predictions of ' + str(others) + ' Other tags.' 


def sanity_check(dir, in_file):
	with open(dir + in_file, 'rb') as fp:
		csv_reader = csv.reader(fp, delimiter=' ', quoting=csv.QUOTE_NONE)
		count = 0
		for row in csv_reader:
			if len(row) < 3:
				print row
				count += 1
		print 'Sanity check complete. < 3 for ' + str(count) + ' rows.\n'


def run_eval_script(dir, in_file):
	os.system('perl ' + \
		my.PERL_EVAL_PATH	+ my.PERL_EVAL_SCRIPT + ' ' +\
		'< ' + dir + in_file)	



