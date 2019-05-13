#!/usr/bin/env python3
# File name: ass3_ex1.py
# Description: script that generates all the information required in exercise 1
# Author: Louis de Bruijn & Friso Stolk
# Date: 09-05-2018

import nltk # v3.4
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet_ic
import operator


def hypernymOf(synset1, synset2):
    """ Returns True if synset2 is a hypernym of 
    synset1, or if they are the same synset. 
    Returns False otherwise. """
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym: 
            return True
        if hypernymOf(hypernym, synset2): 
            return True
    return False


def top_hypernym(synset):
    """ Returns the top hypernym for a synset """
    root = ['abstraction.n.06', 'physical_entity.n.01', 'thing.n.12']

    if synset.hypernyms():
        # synset.root_hypernyms()[0])
        for h in synset.hypernyms():
            hypernym = h.hypernyms()[0]
            if hypernym.name() in root:
                return h.name()
            else:
                return top_hypernym(hypernym)
    else:
        return None


def WordNet_relations(noun_lemmas):
    """ Returns dictionary with nouns that refer to items in synset2 """
    # find correct synsets for three words
    # synset2 = ['relative', 'illness', 'science']
    # for i in synset2:
    #     synsets = wn.synsets(i)
    #     for s in synsets:
    #         print(s, s.definition())


    # retrieve synset for each lemma
    synset2 = ['relative.n.01', 'illness.n.01', 'science.n.01']
    words = defaultdict(list)
    for s in synset2:
        wn_synset2 = wn.synset(s)
        for lemma in noun_lemmas:
            synset = wn.synsets(lemma, pos=wn.NOUN)
            for i in synset:
                if hypernymOf(i, wn_synset2):
                    words[s[:-5]].append(lemma)

    return words


def wordNet_similarity():
    """ Returns a dict with the matching rank items per similarity method """
    brown_ic = wordnet_ic.ic('ic-brown.dat')
    word_pairs = [('car', 'automobile'), ('coast', 'shore'), ('food', 'fruit'), ('journey', 'car'), ('monk', 'slave'), ('moon', 'string')]
    word_rank = ["-".join(item) for item in word_pairs]

    tot = defaultdict(list)

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].path_similarity(wn.synsets(item[1])[0]) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['path'] = matches

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].lch_similarity(wn.synsets(item[1])[0]) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['lch'] = matches

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].wup_similarity(wn.synsets(item[1])[0]) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['wup'] = matches

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].res_similarity(wn.synsets(item[1])[0], brown_ic) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['res'] = matches

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].jcn_similarity(wn.synsets(item[1])[0], brown_ic) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['jcn'] = matches

    sim_rank = { "-".join(item): 
        wn.synsets(item[0])[0].lin_similarity(wn.synsets(item[1])[0], brown_ic) for item in word_pairs }
    ranking = sorted(sim_rank.items(), key=operator.itemgetter(1), reverse=True)
    ranking = [i[0] for i in ranking]
    matches = [i for i, j in zip(word_rank, ranking) if i == j]
    tot['lin'] = matches

    return tot


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

    # print("### Exercise 1: WordNet relations")
    # words = WordNet_relations(noun_lemmas)
    # for key, value in words.items():
    #     print("{0} nouns refer to {1}. The nouns are: {2}".format(len(value), key, value))


    # # Multiple classes [unfinished]
    top_N_class = defaultdict(list)
    for lemma in noun_lemmas:
        synset_list = wn.synsets(lemma, pos=wn.NOUN)
        for synset in synset_list:
            top_N_class[lemma].append(top_hypernym(synset))

    for k, v in top_N_class.items():
        print(k, v)


    # print("### Exercise 3: WordNet similarity")
    # matches = wordNet_similarity()
    # for k, v in matches.items():
    #     print("Similarity measure '{0}' has {1} matches: {2}".format(k, len(v), v))




if __name__ == '__main__':
    main()
