# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import os
import sys
#import settings as my
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--test', nargs='*')
	parser.add_argument('-r', '--run', nargs='*', help='\
		[all - Run entire process]')
	parser.add_argument('-p', '--prep', nargs='*')
	parser.add_argument('-f', '--feat', nargs='?')
	parser.add_argument('-c', '--classi', nargs='?')
	args = parser.parse_args()

	if args.test:
		import src.test as do
		if 'test' in args.test:
			print '\n*** Test, test, test! ***\n'
			do.test()
	if args.prep:
		if 'ami' in args.prep or 'amida' in args.prep:
			import src.prep_amida as prep
			#prep.build_word_dict()
			#prep.build_subj_list()
			#prep.make_data_info()
			#prep.balance_classes()
		if 'yt' in args.prep or 'youtube' in args.prep:
			import src.prep_youtube as prep
			#prep.remane_files('audio', 'wav')
			#prep.remane_files('transcriptions', 'trs')
			#prep.remane_files('_praat', 'csv')
			#prep.build_word_dict()
			#prep.build_utterence_list()
			#prep.make_data_info()
			#prep.balance_classes()
	if args.feat:
		import src.feature_extractor as feat
		#feat.gen_text_feat()
		#feat.gen_char_feat()
		#feat.gen_swn_feat()
		#feat.gen_audio_feat()
		#feat.gen_labels()
	if args.classi:
		import src.classify as classi
		#classi.classify_all()
		classi.plot_charts()

