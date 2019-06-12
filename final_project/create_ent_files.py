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
# pip3 install https://github.com/elyase/geotext/archive/master.zip
from geotext import GeoText # Geotext extracts country and city mentions from text
# pip3 install pycountry
import pycountry # all countries in a list
from nltk.corpus import wordnet as wn
from nltk.tree import Tree
from nltk.wsd import lesk


def get_continuous_chunks(sent):
    '''extract named entities form nltk.ne_chunk'''

    chunked = nltk.ne_chunk(sent)
    named_entities = []
    # we need an index for the word
    for idx, tree_item in enumerate(chunked):

        if type(tree_item) == Tree:
            # because there can be multiple tokens in one id
            idx = idx - 1 + len(tree_item.leaves())

            # print('leaves', i.leaves())
            entity_list = [] # append each tup(token, POS, tag) in here
            for tup in tree_item.leaves(): # tup(token, POS)
                token = tup[0]
                pos = tup[1]
                tag = '-'
                # hardcoding: sometimes it tags months as named entities
                if token not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']: 
                    # only take these into account, not 'JJ'
                    if pos in ['NNS', 'NNP', 'NNPS']:
                        if 'ORGANIZATION' in str(tree_item):
                            tag = 'ORG'
                        if 'PERSON' in str(tree_item):
                            tag = 'PER'
                        if 'GPE' in str(tree_item):
                            tag = 'COU'
                        entity_list.append((idx, token, pos, tag))
            named_entities.append(entity_list)

    # a list of list of tuples that go together: 
    ## [[(9, 'Rugova', 'NNP', 'PER')], [(18, 'European', 'NNP', 'ORG'), (18, 'Union', 'NNP', 'ORG')]
    return named_entities


def create_sentences(path):
    '''create sentences with offsets'''
    sentData = []
    with open(path) as rawFile:
        # read text 
        rawText = rawFile.read()
        # remove newline characters inside text
        rawText = rawText.replace('\n', ' ')
        # create sentences
        sents = nltk.sent_tokenize(rawText)
        # append sentences offsets and sentences
        begin = 0
        for s in sents:
            end = begin + len(s)
            sentData.append((begin, end, s))
            begin = end + 1
    return sentData


def spacy_tagger(sent, nlp):
    '''find named entities based on SpaCy model and return these entities'''
    
    entities = []
    # create nlp pipeline
    doc = nlp(sent)
    # append entity offsets, text and tagged category
    for ent in doc.ents:
        # change SpaCy tags to our category tags
        if ent.label_ not in ['NORP', 'FAC', 'PRODUCT', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']:
            if ent.label_ == 'PERSON': # change PERSON to PER
                entities.append((ent.start_char, ent.end_char, ent.text, 'PER'))
            elif ent.label_ == 'LOC': # Non-GPE locations, mountain ranges, bodies of water.
                entities.append((ent.start_char, ent.end_char, ent.text, 'NAT'))
            elif ent.label_ == 'WORK_OF_ART': #Titles of books, songs, etc.
                entities.append((ent.start_char, ent.end_char, ent.text, 'ENT'))
            elif ent.label_ == 'GPE': # Countries, cities, states.
                # disambiguation between cities and countries
                cit = GeoText(ent.text) # cities
                if cit.cities: # cities
                    entities.append((ent.start_char, ent.end_char, ent.text, 'CIT'))
                elif ent.text in list(pycountry.countries): # countries 
                    entities.append((ent.start_char, ent.end_char, ent.text, 'COU'))

                ## TODO: kijken hoe we disambiguate between CIT and COU
                entities.append((ent.start_char, ent.end_char, ent.text, 'COU'))
            else:
                entities.append((ent.start_char, ent.end_char, ent.text, ent.label_))

    return entities


def categorise_WordNet(lines, begin, end, sent, entities):
    '''finds named entities based on WordNet information and returns the entity'''
    categories = {'ANI': ['animal', 'bird'], 'SPO': ['sport'], 'NAT': ['ocean', 'river', 'mountain', 'crack', 'land']}
    for line in lines:
        # see if line is in the sentence in order to go through lines per sentence 
        if begin <= int(line[1]) <= end:
            token = line[3] # 'turtles' and 'sea' tagged wrong
            tag = line[4]
            if tag in ['NNPS', 'NNS']:
                synsets = wn.synsets(token, pos=wn.NOUN) # creates a list with all found synsets for noun
                if len(synsets) > 1:
                    # let Lesk algorithm choose the correct synset from ambigu results
                    synset = lesk(sent, token, pos=wn.NOUN) # use Lesk algorithm to choose synset
                    # synset = wn.synsets(token, pos=wn.NOUN)[0] # only use the first synset found by WordNet
                    hypernyms = [i for i in synset.closure(lambda s:s.hypernyms())] 
                    # iterate through hypernyms to see whether they match a category
                    for hyp in hypernyms:
                        if str(hyp) != "Synset('public_transport.n.01')": # door categorie 'sport' ging deze ook mee
                            for key, value_list in categories.items():  
                                for cat in value_list:
                                    if cat in str(hyp):
                                        for ent in entities:
                                            # check if NE tagged by NLTK already in entities list (found by SpaCy)
                                            if int(line[0]) == int(ent[0]) and int(line[1]) == int(ent[1]) and token == ent[2]:
                                                break
                                            else:
                                                return (line[0], line[1], token, key)

def nltk_ner_tagger(lines, begin, end, entities):
    '''finds entities tagged by nltk's NER tagger and converts categories '''
    
    ## create NLTK tagged entities
    ne_chunk_input = [] # input needs to be tuple(token, pos) for NLTK NER tagger

    for line in lines:
        # see if line is in the sentence in order to go through lines per sentence 
        if begin <= int(line[1]) <= end:
            ne_chunk_input.append((line[3], line[4]))
    # get NE tagged by NLTK.chunker
    named_entities_list = get_continuous_chunks(ne_chunk_input)
    # a list of list of tuples(token, pos, tag)
    ## [[(9, 'Rugova', 'NNP', 'PER')], [(18, 'European', 'NNP', 'ORG'), (18, 'Union', 'NNP', 'ORG')]
    ne_chunk_input.clear() # return to empty input for next sentence

    
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

        for ne in item:
            # check if index of word matches index of line item
            for idx, line in enumerate(lines):
                # if NER id equals line id and NER token == line token
                if idx == ne[0] and ne[1] == line[3]:
                    # check if the NE from NLTK are already found by SpaCy 
                    if any(line[3] in ent[2] for ent in entities):
                        # NE found in entities, thus break loop
                        break
                    else:
                        # append the missing NE tagged entity to entities
                        return (line[0], line[1], line[3], ne[3])
                        ## TODO hier kunnen we nog mee spelen
                        ## if ne[3] == 'COU' of ne[3] == '-'
                        ## hij tagt alles als 'COU', ook 'CIT'


def create_files(path, model, output_file='.ent.louis'):
    '''create the .ent files based on the model'''

    

    rawPathlist = glob.glob(path + '/en.raw')
    offsetPosList = glob.glob(path + '/en.tok.off.pos')

    for r, p in zip(rawPathlist, offsetPosList):
        print(r, p)

        # append lines from csv.reader to list, because can't iterate over csv.reader
        with open(p) as posFile:
            csvReader = csv.reader(posFile, delimiter=" ")
            lines = [line for line in csvReader]

        entities = []
        # create sentences w/ offsets in tuple
        sentData = create_sentences(r)


        # find our entities 
        for begin, end, sent in sentData:

            #find entities with SpaCy model
            nlp = spacy.load(model) # load the SpaCy model
            spacy_entity = spacy_tagger(sent, nlp) # a list of entities
            if spacy_entity: 
                # print('Appending SpaCy tagged entities', spacy_entity)
                for spacy_ent in spacy_entity:
                    entities.append(spacy_ent)          

            # lets try to find new entities with the NLTK NER tagger
            nltk_entity = nltk_ner_tagger(lines, begin, end, entities)
            if nltk_entity:
                # print('Appending NLTK tagged entities', nltk_entity)
                entities.append(nltk_entity)

            # find entities for categories 'ANI', 'SPO' and 'NAT' with WordNet
            wn_entity = categorise_WordNet(lines, begin, end, sent, entities)
            if wn_entity:
                # print('Appending WordNet tagged entities', wn_entity)
                entities.append(wn_entity)


        # iterate over entities and lines
        for ent in entities:
            for line in lines:
                # check if offsets of entity match ent.tok.off.pos token offsets
                if int(line[0]) == int(ent[0]) and int(line[1]) == int(ent[1]):
                    # print(ent[2], ent[3])
                    line.append(ent[3])


        with open(p + output_file, "w") as parserFile:
            for line in lines:
                # if len(line)>5:
                #     print(line)
                item = ' '.join(line)
                parserFile.write("%s\n" %item)


        print('Succesfully created "{0}" file in directory: {1}'.format(output_file, p + output_file))

def compare(path, output_file):
    '''compare parser file and gold standard file'''

    parserOutput = glob.glob(path + '/en.tok.off.pos' + output_file)
    goldStandard = glob.glob(path + '/en.tok.off.pos.ent')

    score = []

    for p, g in zip(parserOutput, goldStandard):

        parserLines = []
        with open(p) as parserFile:
            csvReader = csv.reader(parserFile, delimiter=" ")
            for line in csvReader:
                if len(line) > 5:
                    parserLines.append([line[2], line[3], line[5]])

        goldLines = []
        with open(g) as goldFile:
            csvReader = csv.reader(goldFile, delimiter=" ")
            for line in csvReader:
                if len(line) > 5:
                    goldLines.append([line[2], line[3], line[5]]) # don't append the Wikipedia link


        print(p)
        print('parser', parserLines)
        print('gold', goldLines)  
        print()  


        # hier kunnen we al die precision en recall uitrekenen
        # en de f1 score etc

        tag = 0 # the parser tagged the same entity
        cat = 0 # the parser also tagged the same entity with the same category
        for gold in goldLines:
            for pars in parserLines:
                if gold[0] == pars[0]:
                    tag += 1
                    if gold[2] == pars[2]:
                        print(pars, gold)
                        cat += 1


        missed = len(parserLines) - len(goldLines) # hoeveel tags we missen..

        score.append((p[:13], tag, cat, missed))
    return score


def main():
    '''Create parser file and compare it to the gold standard file'''

    path = 'dev/*/*'                            # set to 'dev/*/*' for all files
    # model = "en_core_web_sm"                    # SpaCy English model
    # model = os.getcwd() + '/spacy_model'        # our own model
    model = os.getcwd() + '/spacy_modelv2'      # our own model + SpaCy English model
    output_file = '.ent.louis'                  # output file endings
    
    ## run it
    create_files(path, model, output_file)

    ## compare gold standard and parser files
    # print(compare(path, output_file))


if __name__ == '__main__':
    main()
