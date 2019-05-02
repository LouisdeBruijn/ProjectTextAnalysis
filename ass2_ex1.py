#!/usr/bin/env python3
# File name: ass2_ex1.py
# Description: script that generates all the information required in exercise 1
# Author: Louis de Bruijn & Friso Stolk
# Date: 02-05-2018

import nltk # v3.4
from nltk.collocations import *
from nltk.metrics.spearman import *

def main():

    # Read the text
    path = "holmes.txt"
    f = open(path)
    rawText = f.read()
    f.close()

    sents = nltk.sent_tokenize(rawText) # tokenize rawText to sentences

    # create tokens per sentence, because nltk.word_tokenize needs sentences as input
    tokens_s = [nltk.word_tokenize(s) for s in sents] # a list of lists: sentences w/ tokens
    
    # but for collocations we need not a list of tokens per sentence, but a list of tokens per rawText   
    tokens_t = [t for s in tokens_s for t in s] # a list of tokens 

    bigram_measures = nltk.collocations.BigramAssocMeasures() # create bigram measures object
    finder = BigramCollocationFinder.from_words(tokens_t) # create finder object
    text = nltk.Text(tokens_t) # create a text object

    # print("### Exercise 1: top 20 collocations w/ collocations() function")
    # print(text.collocations(20)) # top 20 collocations w/ collocations()

    # print("### Exercise 1a: top 20 collocations w/ PMI")
    # print(finder.nbest(bigram_measures.pmi, 20)) # top 20 collocations w/ PMI

    # print("### Exercise 1b: top 20 collocations w/ chi-square")
    # print(finder.nbest(bigram_measures.chi_sq, 20)) # top 20 collocations w/ chi-square

    # print("###")
    # print("### Exercise 1c: MAG FRISO DOEN: 20 > 40 veranderen, dan zie je wel verschil")
    # print("### Exercise 1c: top 20 collocations without any association measure")
    # print(finder.nbest(bigram_measures.raw_freq, 20)) # top 20 collocations w/ chi-square
    # print("###")

    print("### Exercise 1d: Calculate Spearman's coefficient") 
    pmi = finder.score_ngrams(bigram_measures.pmi)
    chi_sq = finder.score_ngrams(bigram_measures.chi_sq)
    raw_freq = finder.score_ngrams(bigram_measures.raw_freq)

    print("Spearman correlation for PMI and chi-square: {0}".format(round(spearman_correlation(
        list(ranks_from_scores(pmi)),list(ranks_from_scores(chi_sq))),3)))
    print("Spearman correlation for PMI and raw_freq: {0}".format(round(spearman_correlation(
        list(ranks_from_scores(pmi)), list(ranks_from_scores(raw_freq))),3)))
    print("Spearman correlation for chi-square and raw_freq: {0}".format(round(spearman_correlation(
        list(ranks_from_scores(chi_sq)), list(ranks_from_scores(raw_freq))),3)))


if __name__ == '__main__':
    main()
