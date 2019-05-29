#!/usr/bin/env python3
# File name: disambiguation.py
# Description: 
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 29-05-2018

import wikipedia
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from collections import defaultdict
# from nltk import word_tokenize
# from nltk import pos_tag

def main():
    PAGE_NAME = "New York City"
    page = wikipedia.page(PAGE_NAME)
    raw_text = page.content
    
    sents = nltk.sent_tokenize(raw_text) # tokenize rawText to sentences

    # create tokens per sentence, because nltk.word_tokenize needs sentences as input
    tokens_s = [nltk.word_tokenize(s) for s in sents] # a list of lists: sentences w/ tokens
    
    # but for collocations we need not a list of tokens per sentence, but a list of tokens per rawText   
    tokens_t = [t for s in tokens_s for t in s] # a list of tokens
    
    pos_tags = nltk.pos_tag(tokens_t)
    
    sent_dict = defaultdict(list)
    j = k = 0
    key = sents[0]
    for i in range(len(pos_tags)):
        if j == len(tokens_s[k]):
            k += 1
            j = 0
            key = sents[k]
            sent_dict[key] = []
        #print(tokens_s[k][j])
        #print(pos_tags[i])
        #print('\n')
        sent_dict[key].append(pos_tags[i])
        j += 1
        
    print(sent_dict)
    
    #nouns = []
    #for i in range(len(pos_tags)):
    #    if pos_tags[i][1] == 'NN' or pos_tags[i][1] == 'NNP' or pos_tags[i][1] == 'NNS' or pos_tags[i][1] == 'NNPS':
    #        nouns.append(pos_tags[i][0])
    
    #ambiguous_nouns = {}
    #for noun in nouns:
    #    if len(wordnet.synsets(noun, 'n')) > 1:
    #    ambiguous_nouns[noun] = lesk(
            
    #print(len(ambiguous_nouns))
    

if __name__ == "__main__":
    main()