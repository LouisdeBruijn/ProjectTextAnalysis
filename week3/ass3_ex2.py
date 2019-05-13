#!/usr/bin/env python3
# File name: ass3_ex2.py
# Description: script that generates all the information required in exercise 2
# Author: Louis de Bruijn & Friso Stolk
# Date: 09-05-2018

import nltk # v3.4
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet_ic
from nltk.parse import CoreNLPParser
import operator


def main():

    # Read the text
    path = "ada_lovelace.txt"
    f = open(path)
    rawText = f.read()
    f.close()

    sents = nltk.sent_tokenize(rawText) # tokenize rawText to sentences
    tokens_s = [nltk.word_tokenize(s) for s in sents] # a list of lists: sentences w/ tokens
    tokens_t = [t for s in tokens_s for t in s] # a list of tokens 
    pos_tags = nltk.pos_tag(tokens_t)

    # create a list of nouns (recognized by their POS-tag)
    nouns = []
    for i in range(len(pos_tags)):
        if pos_tags[i][1] == 'NN' or pos_tags[i][1] == 'NNP' or pos_tags[i][1] == 'NNS' or pos_tags[i][1] == 'NNPS':
            nouns.append(pos_tags[i][0])

    # lemmatize the nouns
    lemmatizer = WordNetLemmatizer()
    noun_lemmas = [lemmatizer.lemmatize(noun, wn.NOUN) for noun in nouns]


    print("### Exercise 1 & 2, changing depending on server properties")
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    nec_list = list(ner_tagger.tag(tokens_t))
    nec_dict = {} # Named entiny: class
    nec_reversedict = defaultdict(list) # Class: [list of named entities]
    for (name, nec) in nec_list:
        if not nec == 'O':
            nec_dict[name] = nec
            nec_reversedict[nec].append(name)
    for e in nec_reversedict:
        print("Named Entity Class '{}' was found {} times: {}".format(e, len(nec_reversedict[e]), nec_reversedict[e]))

    print("### Exercise 3")
    for noun in nouns:
        if noun in nec_dict:
            print("{}: {}".format(noun, nec_dict[noun]))
        else:
            print("{}: {}".format(noun, lemmatizer.lemmatize(noun, wn.NOUN)))

if __name__ == '__main__':
    main()
