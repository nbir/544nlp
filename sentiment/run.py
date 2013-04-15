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
	parser.add_argument('-t', '--test', nargs='*', help='\
		[test - Test, test, test!]')
	parser.add_argument('-r', '--run', nargs='*', help='\
		[all - Run entire process]')
	args = parser.parse_args()

	if args.test:
		import src.test as do
		if 'test' in args.test:
			print '\n*** Test, test, test! ***\n'
			do.test()
