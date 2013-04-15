# -*- coding: utf-8 -*-

# 544 NLP Term Project
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE

from src.sentiwordnet import *

def test():
	lex = LexiconSA()
	lex.test()
	#lex.build()
	#h = lex.senti_words(['slow', 'party', 'crack', 'car'])
	#h = lex.senti_sent('What the bloody hell is wrong with you?')
	#print h