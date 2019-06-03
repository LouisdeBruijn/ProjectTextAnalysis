#!/usr/bin/env python3
# File name: disambiguation.py
# Description: Provide disambiguation for 
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 29-05-2018

import wikipedia
import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from collections import defaultdict
# from nltk import word_tokenize
# from nltk import pos_tag


def main():

    wiki_urls = [ 'https://en.wikipedia.org/wiki/North_Waziristan', 
        'https://en.wikipedia.org/wiki/United_States_Congress', 
        'https://en.wikipedia.org/wiki/South_Africa', 
        'https://en.wikipedia.org/wiki/Iraq', 
        'https://en.wikipedia.org/wiki/Commonwealth_of_Nations'
        ]

    wiki_names = [ 'North Waziristan', 
        'United States Congress', 
        'South Africa', 
        'Iraq', 
        'Commonwealth of Nations'
        ]
    
    histogram = defaultdict(int)
    words_per_wiki = []

    for name in wiki_names:
        page = wikipedia.page(name)
        raw_text = page.content
        poly_words = 0
        total_words = 0
        
        sents = nltk.sent_tokenize(raw_text) # tokenize rawText to sentences
        # create tokens per sentence, because nltk.word_tokenize needs sentences as input
        tokens_s = [nltk.word_tokenize(s) for s in sents] # a list of lists: sentences w/ tokens
        # but for collocations we need not a list of tokens per sentence, but a list of tokens per rawText   
        tokens_t = [t for s in tokens_s for t in s] # a list of tokens
        # POS tagging tokens
        pos_tags = nltk.pos_tag(tokens_t)
        
        # create dictionary with sentences as keys and tokens as value list
        sent_dict = defaultdict(list)
        j = k = 0
        key = sents[0]
        for i in range(len(pos_tags)):
            if j == len(tokens_s[k]):
                k += 1
                j = 0
                key = sents[k]
                sent_dict[key] = []
            if pos_tags[i][1] == 'NN' or pos_tags[i][1] == 'NNP' or pos_tags[i][1] == 'NNS' or pos_tags[i][1] == 'NNPS':
                # print(pos_tags[i])
                sent_dict[key].append(pos_tags[i])
            j += 1
            
        # extract ambiguous nouns and find most relevant definiont using Lesk
        for key, value in sent_dict.items():
            for (token,pos) in value:
                # print(token, pos)
                total_words += 1
                if len(wn.synsets(token, pos=wn.NOUN)) > 1:
                    histogram[len(wn.synsets(token, pos=wn.NOUN))] += 1
                    poly_words += 1
                    # print(wn.synsets(token, pos=wn.NOUN))
                    print('For the following word:', token)
                    print('The Lesk algorithm shows this is the best definition:')
                    print(lesk(key, token, pos=wn.NOUN))
                    print()
        words_per_wiki.append(poly_words / total_words)
        
    for em in words_per_wiki:
        print(em)
        
    print(histogram)
    total_words = 0
    total_senses = 0
    for key, value in histogram.items():
        total_words += value
        total_senses += key * value
    print(total_senses / total_words)


if __name__ == "__main__":
    main()

