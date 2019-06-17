#!/usr/bin/python3
# File name: create_ent_files.py
# Description: Creates .ent files with annoted categories
# Author: Louis de Bruijn
# Date: 11-06-2018

import glob
import csv
import os
import nltk
import spacy
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.tree import Tree
from nltk.wsd import lesk
from collections import Counter
from collections import defaultdict
from nltk.metrics import ConfusionMatrix
# pip install -U pywsd
from pywsd.lesk import simple_lesk, adapted_lesk, cosine_lesk

def get_continuous_chunks(sent):
    '''extract named entities form nltk.ne_chunk'''

    chunked = nltk.ne_chunk(sent)
    named_entities = []
    # we need an index for the word
    index = -1
    for tree_item in chunked:
        index += 1
        if type(tree_item) == Tree:
            # because there can be multiple tokens in one id
            index = index - 1 + len(tree_item.leaves())
            # print('leaves', i.leaves())
            entity_list = [] # append each tup(token, POS, tag) in here
            for tup in tree_item.leaves(): # tup(token, POS)
                token = tup[0]
                pos = tup[1]
                tag = '-'
                # hardcoding: sometimes it tags months as named entities
                if token not in ['Mr.', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']: 
                    # only take these into account, not 'JJ'
                    if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
                        if 'ORGANIZATION' in str(tree_item):
                            tag = 'ORG'
                        if 'PERSON' in str(tree_item):
                            tag = 'PER'
                        if 'GPE' in str(tree_item):
                            tag = 'COU'
                        entity_list.append((index, token, pos, tag))
            named_entities.append(entity_list)

    # a list of list of tuples that go together: 
    ## [[(9, 'Rugova', 'NNP', 'PER')], [(18, 'European', 'NNP', 'ORG'), (18, 'Union', 'NNP', 'ORG')]
    return named_entities


def gpe_disambiguation(token):
    '''disambiguate between cities and countries'''
    with open('GPE/countries.txt') as countryFile:
        for line in countryFile:
            if token in line:
                return 'COU'

    with open('GPE/cities.txt') as cityFile:
        csvReader = csv.reader(cityFile, delimiter=",")
        for line in csvReader:
            if token in line[1] or token in line[2]: #lowercase and uppercase city names
                return 'CIT'

    return 'COU'


def spacy_tagger(raw, nlp):
    '''find named entities based on SpaCy model and return these entities'''
    
    new_entities = []
    # create nlp pipeline
    doc = nlp(raw)
    # append entity offsets, text and tagged category
    for ent in doc.ents:

        # offsets have been adjusted to fit both double entities and single
        b = 0 + ent.start_char
        e = 0
        # (125, 132, 'Benazir', 'PER'), (133, 139, 'Bhutto', 'PER')
        for entit in ent.text.split():
            e = b + len(entit)
            # change SpaCy tags to our category tags
            if ent.label_ not in ['NORP', 'EVENT', 'FAC', 'PRODUCT', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']:

                # NORP = 'Israeli' police, 'Muslim' people etc.
                # if we tag NORP as ORG, the data shows that it is correct 14 times and incorrect 71 times, so let's not include
                # if ent.label_ == 'NORP':
                #     label = 'EXTRA'
                if ent.label_ in ['COU', 'GPE']: # Countries, cities, states.
                    # disambiguate between countries and cities
                    label = gpe_disambiguation(ent.text)
                elif ent.label_ == 'PERSON': # change PERSON to PER
                    label = 'PER'
                elif ent.label_ == 'LOC': # Non-GPE locations, mountain ranges, bodies of water.
                    label = 'NAT'
                elif ent.label_ == 'WORK_OF_ART': # Titles of books, songs, etc.
                    label = 'ENT'
                else:
                    label = ent.label_

                new_entities.append((str(b), str(e), entit, label))
            # for ent offsets
            e += 1
            b = e

    return new_entities


def nltk_ner_tagger(lines):
    '''finds entities tagged by nltk's NER tagger and converts categories '''
    
    new_entities = []

    ## create NLTK tagged entities
    ne_chunk_input = [] # input needs to be tuple(token, pos) for NLTK NER tagger
    for line in lines:
        ne_chunk_input.append((line[3], line[4]))

    # get NE tagged by NLTK.chunker
    named_entities_list = get_continuous_chunks(ne_chunk_input)
    ## [[(9, 'Rugova', 'NNP', 'PER')], [(18, 'European', 'NNP', 'ORG'), (18, 'Union', 'NNP', 'ORG')]


    ## check if item already tagged by SpaCy, and append otherwise
    for item in named_entities_list:
        # this is to rewrite my index, because it get's tagged as index 19 for both items:
        ## [(19, 'European', 'NNP', 'ORG'), (19, 'Union', 'NNP', 'ORG')
        if len(item) > 1:
            new_item = []
            index = 1 - len(item)
            for tup in item:
                index += tup[0]
                break
            for tup in item:
                tup = (index, tup[1], tup[2], tup[3])
                new_item.append(tup)
                index += 1
            item = new_item
        # now it is:
        ## [(18, 'European', 'NNP', 'ORG'), (19, 'Union', 'NNP', 'ORG')

        cnt = 0
        for ne in item:
            # check if index of word matches index of line item
            for line in lines:
                # # create index of 0 every new line
                if int(line[0]) == 0:
                    cnt = 0
                # if NER id equals line id and NER token == line token
                # then that tagged entity equals the line entity
                # and thus we can append it
                if cnt == ne[0] and ne[1] == line[3]:
                    if ne[3] == 'COU':
                        # disambiguate between countries and cities
                        new_entities.append((line[0], line[1], line[3], gpe_disambiguation(line[3])))
                    else:
                        # append the missing NE tagged entity to entities
                        new_entities.append((line[0], line[1], line[3], ne[3]))
                cnt += 1

    return new_entities


def categorise_WordNet(lines, doc):
    '''finds named entities based on WordNet information and returns the entity'''
    categories = {'ANI': ['animal', 'bird'], 'SPO': ['sport'], 'NAT': ['ocean', 'river', 'mountain', 'crack', 'land']}
    for line in lines:
        token = line[3]
        tag = line[4]
        if tag in ['NN', 'NNPS', 'NNS']:
            synsets = wn.synsets(token, pos=wn.NOUN) # creates a list with all found synsets for noun
            if len(synsets) > 1:
                # let Lesk algorithm choose the correct synset from ambigu results
                # use any of the following Lesk-based algorithms to disambiguate synset
                # so far adapted_lesk is the best: does not tag 'bird(s)', services' & 'workers', but does tag 'soldiers' and 'survivors' 
                # synset = adapted_lesk(sent, token, pos='NOUN') # simple_lesk(), cosine_lesk(), adapted_lesk() or just lesk() from NLTK
                synset = adapted_lesk(doc, token, pos='NOUN')
                # find hypernyms for this synset
                hypernyms = [i for i in synset.closure(lambda s:s.hypernyms())] 
                # iterate through hypernyms to see whether they match a category
                for hyp in hypernyms:
                    if str(hyp) != "Synset('public_transport.n.01')" and str(hyp) != "Synset('sports_equipment.n.01')": # beide is geen sport
                        for key, value_list in categories.items():  
                            for cat in value_list:
                                if cat in str(hyp):
                                    return (line[0], line[1], token, key)


def create_files(path, model, output_file='.ent.louis'):
    '''create the .ent files based on the model'''

    rawPathlist = glob.glob(path + '/en.raw')
    offsetPosList = glob.glob(path + '/en.tok.off.pos')

    for p in offsetPosList:
        print(p)

        # create document list items form rawText
        doc = []

        # append lines
        with open(p) as posFile:
            lines = [line.rstrip().split() for line in posFile]
            for line in lines:
                # directly append if line[3] is any of the following substrings
                substrings = ["'", ":", ".", ",", "-"]
                if any(string in line[3] for string in substrings):
                    doc.append(doc[-1]+line[3])
                    del doc[-2]
                else:
                    doc.append(line[3])

        # create rawText
        doc = ' '.join(doc)
        # print(doc)

        entities = []

        #find entities with SpaCy model
        nlp = spacy.load(model) # load the SpaCy model
        spacy_entity = spacy_tagger(doc, nlp) # a list of entities
        if spacy_entity: 
            print('Appending SpaCy tagged entities', spacy_entity)
            for spacy_ent in spacy_entity:
                entities.append(spacy_ent)

        # lets try to find new entities with the NLTK NER tagger
        nltk_entity = nltk_ner_tagger(lines)
        if nltk_entity:
            print('Appending NLTK tagged entities', nltk_entity)
            for nltk_ent in nltk_entity:
                entities.append(nltk_ent)

        # find entities for categories 'ANI', 'SPO' and 'NAT' with WordNet
        wn_entity = categorise_WordNet(lines, doc)
        if wn_entity:
            print('Appending WordNet tagged entities', wn_entity)
            entities.append(wn_entity)

        # out of all NER taggers, choose the tag
        dic = defaultdict(list)
        for (_, _, token, tag) in entities:
            dic[token].append(tag)

        for key, value in dic.items():
            for idx, (b, e, token, tag) in enumerate(entities):
                if key == token:
                    # choose the used tag, if two tags same amount, choose first
                    tag = max(value, key=value.count)
                    # delete entity with incorrect tag
                    del entities[idx]
                    # insert entitiy with most used tag
                    entities.insert(idx, (b, e, key, tag))

        # make the items unique
        entities = list(set(entities))

        # if token is already in entity, append it with same tag
        for ent in entities:
            for line in lines:
                # check if entity-token is in line
                if ent[2] == line[3] and ent[0] != line[0] and ent[1] != line[1]:
                    # check if this line is not already in entities
                    if (line[0], line[1], line[3], ent[3]) not in entities:
                        # tokens such "'s" or "The" or "and" were once tagged as entity, but these are not ALWAYS entities
                        if line[4] not in ['POS', 'DT', 'CC', 'IN']:
                            # append the line + earlier entity tagged category
                            entities.append((line[0], line[1], line[3], ent[3]))
                            # lost of files have wrong offsets... which means that a lot of tokens get in here
                            print('### WRONG OFFSETS IN FILE ? ###')

        # append entity tag to the line
        for ent in entities:
            for line in lines:
                # check if offsets of entity match ent.tok.off.pos token offsets
                if int(line[0]) == int(ent[0]) and int(line[1]) == int(ent[1]):
                    line.append(ent[3])


        # write lines the an output file
        with open(p + output_file, "w") as parserFile:
            for line in lines:
                # if len(line)>5:
                #     print(line)
                item = ' '.join(line)
                parserFile.write("%s\n" %item)

        print('Succesfully created "{0}" file in directory: {1}'.format(output_file, p + output_file))


def measures(path, output_file):
    '''compare parser file and gold standard file'''
    parserOutput = glob.glob(path + '/en.tok.off.pos' + output_file)
    goldStandard = glob.glob(path + '/en.tok.off.pos.ent')


    # de lines appenden aan een lijst en dat schrijven naar errors.txt
    errors = []

    for p, g in zip(parserOutput, goldStandard):
        print(p, g)

        labels = set()

        parser = []
        gold = []
        parserLines = []
        goldLines = []

        with open(p) as parserFile:
            for line in parserFile:
                line = line.rstrip().split()
                parserLines.append(line)
                if len(line) > 5:
                    labels.add(line[5])
                    parser.append(line[5])
                else:
                    parser.append(' ')
                    
        with open(g) as goldFile:
            for line in goldFile:
                line = line.rstrip().split()
                goldLines.append(line)
                if len(line) > 5:
                    labels.add(line[5])
                    gold.append(line[5]) # don't append the Wikipedia link

                    # # TODO: for testing WordNet!!!!
                    # if line[5] in ['ANI', 'SPO', 'ENT']:
                    #     print(line)

                else:
                    gold.append(' ')


        for p, g in zip(parserLines, goldLines):
            if p == g[:6]:
                pass
            else:
                print(p, g[:6])
                errors.append("{0}\t\t{1}".format(p, g[:6]))

                # # to check WordNet entities
                # if len(p) > 5:
                #     if p[5] in ['ANI', 'SPO', 'ENT']:
                #         print(p, g[:6])
                # if len(g) > 5:
                #     if g[5] in ['ANI', 'SPO', 'ENT']:
                #         print(p, g[:6])

        print('The labels', labels, '\n')

        cm = ConfusionMatrix(gold, parser)
        print(cm)

        true_positives = Counter()
        false_negatives = Counter()
        false_positives = Counter()

        for i in labels:
            for j in labels:
                if i == j:
                    true_positives[i] += cm[i,j]
                else:
                    false_negatives[i] += cm[i,j]
                    false_positives[j] += cm[i,j]

        print("TP:", sum(true_positives.values()), true_positives)
        print("FN:", sum(false_negatives.values()), false_negatives)
        print("FP:", sum(false_positives.values()), false_positives)
        print() 

        for i in sorted(labels):
            if true_positives[i] == 0:
                fscore = 0
            else:
                precision = true_positives[i] / float(true_positives[i]+false_positives[i])
                recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
                fscore = 2 * (precision * recall) / float(precision + recall)
            print(i, fscore)

    print('length of errors', len(errors))

    # write erronerous lines to an error file
    # errors = with NORP as 'EXTRA' tagged in SpaCy
    # errors2 = SpaCy English model
    # errors3 = own model + SpaCy English model
    with open('errorsnext.txt', "w") as errorFile:
        for error in errors:
            errorFile.write("%s\n" %error)

def main():
    '''Create parser file and compare it to the gold standard file'''

    path = 'dev/*/*'                            # set to 'dev/*/*' for all files
    model = "en_core_web_sm"                    # SpaCy English model
    # model = os.getcwd() + '/spacy_model'        # our own model
    # model = os.getcwd() + '/spacy_modelv2'      # our own model + SpaCy English model
    output_file = '.ent.louis4'                  # output file endings

    ## run it
    create_files(path, model, output_file)

    ## compare gold standard and parser files
    # measures(path, output_file)


if __name__ == '__main__':
    main()
