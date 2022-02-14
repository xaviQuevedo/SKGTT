import re 
import string 
import nltk 

#from spacy.lang.en import English
import spacy
#import textacy


import pandas as pd 
import numpy as np 
import math 
from tqdm import tqdm 

from spacy.matcher import Matcher, DependencyMatcher
from spacy.tokens import Span 
from spacy import displacy

from collections import Counter, OrderedDict


class AnalisisTexto:
	global nlp 
	nlp = spacy.load("en_core_web_sm")

	def get_entities(self, sent):
	  ## chunk 1
	  ent1 = ""
	  ent2 = ""

	  prv_tok_dep = ""    # dependency tag of previous token in the sentence
	  prv_tok_text = ""   # previous token in the sentence

	  prefix = ""
	  modifier = ""

	  #############################################################
	  
	  for tok in nlp(sent):
	    ## chunk 2
	    # if token is a punctuation mark then move on to the next token
	    if tok.dep_ != "punct":
	      # check: token is a compound word or not
	      if tok.dep_ == "compound":
	        prefix = tok.text
	        # if the previous word was also a 'compound' then add the current word to it
	        if prv_tok_dep == "compound":
	          prefix = prv_tok_text + " "+ tok.text
	      
	      # check: token is a modifier or not
	      if tok.dep_.endswith("mod") == True:
	        modifier = tok.text
	        # if the previous word was also a 'compound' then add the current word to it
	        if prv_tok_dep == "compound":
	          modifier = prv_tok_text + " "+ tok.text
	      
	      ## chunk 3
	      if tok.dep_.find("subj") == True:
	        ent1 = modifier +" "+ prefix + " "+ tok.text
	        prefix = ""
	        modifier = ""
	        prv_tok_dep = ""
	        prv_tok_text = ""      

	      ## chunk 4
	      if tok.dep_.find("obj") == True:
	        ent2 = modifier +" "+ prefix +" "+ tok.text
	        
	      ## chunk 5  
	      # update variables
	      prv_tok_dep = tok.dep_
	      prv_tok_text = tok.text
	  #############################################################

	  return [ent1.strip(), ent2.strip()]



	def get_relation(selft, sent):

	  doc = nlp(sent)

	  # Matcher class object 
	  matcher = Matcher(nlp.vocab)

	  #define the pattern 
	  pattern = [{'DEP':'ROOT'}, 
	            {'DEP':'prep','OP':"?"},
	            {'DEP':'agent','OP':"?"},  
	            {'POS':'ADJ','OP':"?"}] 

	  matcher.add("matching_1",[pattern]) 

	  matches = matcher(doc)
	  if len(matches):
	  	k = len(matches) - 1
	  	span = doc[matches[k][1]:matches[k][2]]
	  	return(span.text)
	  else:
	  	return None