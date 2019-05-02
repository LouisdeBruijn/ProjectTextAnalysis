#!/usr/bin/env python3
# File name: week1.py
# Description: script that generates all the information required in exercise 1
# Author: Louis de Bruijn
# Date: 23-04-2018

import nltk # v3.4
from operator import itemgetter

def top_n_freq(items, n):
    '''returns the top N frequent items'''
    fdist = nltk.FreqDist(items)
    sorted_list = sorted(fdist.items(), key=itemgetter(1), reverse=True)
    return sorted_list[:n]


def main():

    # Read the text
    path = "holmes.txt"
    f = open(path)
    rawText = f.read()
    f.close()

    # Split the text up into sentences
    """ sent_tokenize calls the NLTK's currently
    recommended sentence tokenizer to tokenize sentences
    in the given text. Currently, this uses
    PunktSentenceTokenizer.
    """
    sents = nltk.sent_tokenize(rawText)

    print("### Exercise 1a: the longest sentence")
    print(max(sents, key=len)) # print the longest sentence
    
    print("### Exercise 1b: the shortest sentence")
    print(min(sents, key=len)) # print the shortest sentence

    print("### Exercise 1c: the distribution of sentences in terms of length")
    distribution = {}
    for sent in sents: 
        distribution[len(sent)] = distribution.get(len(sent), 0)+1 # counter
    sorted_list = sorted(distribution.items(), key=itemgetter(0), reverse=False) # sort the distribution from high to low
    for item in sorted_list:
        print("{0} {1} {2} {3} {4}.".format('The sentence with length', item[0] , 'occurs', item[1], 'times' ))

    print("### Exercise 1d: average length of sentences in the whole document")
    print("The average length of sentences in this document is {0}".format(round(sum(map(len, sents) ) / len(sents),3)))

    """ Use NLTK's currently recommended word
    tokenizer to tokenize words in the given sentence.
    Currently, this uses TreebankWordTokenizer.
    This tokenizer should be fed a single sentence at a time.
    """
    tokens = nltk.word_tokenize(rawText) # tokenize text

    print("### Exercise 2a: character types")
    fdist = nltk.FreqDist() # initalize frequency distribution
    for token in tokens:
        fdist.update(token) # append to frequency distribution
    # print the number of word types
    print("{0} {1} {2}.".format('There are', len(fdist.keys()), 'character types in this doc'))
    # print alphabetically sorted distribution    
    print("The first 30 alphabetically sorted character types are:")
    distr = sorted(fdist.items(), key=itemgetter(0), reverse=False)
    print(distr[:30])

    print("### Exercise 2a: word types")
    fdist = nltk.FreqDist(tokens) # create frequency distribution
    # print the number of word types
    print("{0} {1} {2}.".format('There are', len(fdist.keys()), 'word types in this doc'))
    # print alphabetically sorted distribution
    distr = sorted(fdist.items(), key=itemgetter(0), reverse=False)
    print("The first 30 alphabetically sorted word types are:")
    print(distr[:30])


    print("### Exercise 2c: top-20 character-level unigrams, bigrams and trigrams")
    char = []
    for token in tokens:
        for ch in token:
            char.append(ch)
    print("Character unigrams", top_n_freq(char, 20)) # unigrams
    print("Character bigrams", top_n_freq(nltk.bigrams(char), 20)) # bigrams
    print("Character trigrams", top_n_freq(nltk.trigrams(char), 20)) # trigrams

    print("### Exercise 2c: top-20 word-level unigrams, bigrams and trigrams")
    print("Word unigrams", top_n_freq(tokens, 20)) # unigrams
    print("Word bigrams", top_n_freq(nltk.bigrams(tokens), 20)) # bigrams
    print("Word trigrams", top_n_freq(nltk.trigrams(tokens), 20)) # trigrams

    ####
    # 2D: dit is nu niet meer op zins niveau. Dus hij pakt ook ['zins_afluister', 'volgende_zins_woord'] bij bigrams
    ###

if __name__ == '__main__':
    main()

