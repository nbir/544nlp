# -*- coding: utf-8 -*-

# Web Page Clustering of Ambiguous Names - 544 NLP Assignment2
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

import os
import sys
import settings as my
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--test', nargs='*', help='\
		[test - Test, test, test!]')
	parser.add_argument('-r', '--run', nargs='*', help='\
		[all - Run entire process]')
	args = parser.parse_args()

	if args.test:
		import bin.eval as do
		if 'test' in args.test:
			print '\n*** Test, test, test! ***\n'
			do.test()

	if args.run:
		import bin.prep as prep
		import bin.feature_extractor as feat
		import bin.cluster as cluster
		import bin.eval as eval

		if 'all' in args.run:
			names = os.listdir('data/' + my.DATA_FOLDER + '/webpages/')
			if '.DS_Store' in names:
				names.remove('.DS_Store')
			print names
			for name in names:
				print '\n*** NOW PERFORMING: %s ***' % (name)

				print 'Cleaning HTML documents'
				prep.clean_html_docs(name)

				print 'Tokenizing documents'
				prep.tokenize_docs(name)

				print 'Generating lexicons'
				prep.generate_lexicons(name)

				print 'Generating feature matrix'
				feat.generate_feature_mat(name)

				print 'Generating clusters'
				cluster.generate_clusters(name)

			print 'Generating results'
			eval.generate_results()
