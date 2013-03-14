# -*- coding: utf-8 -*-

# Named Entity Recognizer - 544 NLP Assignment1
#
# Copyright (C) 2013, Nibir Bora
# Author: Nibir Bora <nbora@usc.edu>
# URL: <http://nibir.me>
# For license information, see LICENSE


import settings as my
import re

##
# token			=		[<actual-word>, <POS-tag> [, <class-label>]]
# sentence	=		[<token> [, <token> [, <token> ...]]]
##

def is_p_noun(token):
	return (1 if token[1] in my.POS_PROPER_NOUN_LIST else 0)

def position(sentence_len, word_position):
	return (int(round(float(word_position)/float(sentence_len), 1) * 10))

def init_cap(token):
	reg = re.compile('^[A-Z][^A-Z]')
	return (1 if reg.match(token[0]) != None else 0)

def all_cap(token):
	reg = re.compile('^[A-Z]+$')
	return (1 if reg.match(token[0]) != None else 0)

def prev_word_cap(sentence, word_position):
	return (0 if word_position-1 < 0 else init_cap(sentence[word_position-1]))

def next_word_cap(sentence, word_position):
	return (0 if word_position+1 >= len(sentence) else init_cap(sentence[word_position+1]))

def next_word_verb(sentence, word_position):
	return (0 if word_position+1 >= len(sentence) else 1 if sentence[word_position+1][1] in my.POS_VERB_LIST else 0)

def is_symbol(token):
	reg = re.compile('^[\W]+$')
	return (1 if reg.match(token[0]) != None else 0)

def prev_trigger_per(sentence, word_position):
	return (0 if word_position-1 < 0 else 1 if sentence[word_position-1][0].strip() in my.TRIGGER_LIST_PER_PREV else 0)

def prev_trigger_org(sentence, word_position):
	return (0 if word_position-1 < 0 else 1 if sentence[word_position-1][0].strip().lower() in my.TRIGGER_LIST_ORG_PREV else 0)

def next_trigger_org(sentence, word_position):
	return (0 if word_position+1 >= len(sentence) else 1 if sentence[word_position+1][0].strip().lower() in my.TRIGGER_LIST_ORG_NEXT else 0)

def prev_trigger_loc(sentence, word_position):
	return (0 if word_position-1 < 0 else 1 if sentence[word_position-1][0].strip().lower() in my.TRIGGER_LIST_LOC_PREV else 0)

def in_gaz(token, gaz):
	return (1 if token[0] in gaz else 0)

def length(token):
	return len(token[0].strip())

def is_prev_ne(sentence_feat_vec, word_position):
	return (-1 if word_position-1 < 0 else sentence_feat_vec[word_position-1][11])

def is_next_ne(sentence_feat_vec, word_position):
	return (-1 if word_position+1 >= len(sentence_feat_vec) else sentence_feat_vec[word_position+1][11])