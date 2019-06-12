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

def get_continuous_chunks(sent):
    '''extract named entities form nltk.ne_chunk'''
    chunked = nltk.ne_chunk(sent)
    named_entities = []
    for i in chunked:
        if type(i) == Tree:
            for token, tag in i.leaves():
                # hardcoding: sometimes it tags months as named entities
                if token not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']: 
                    # only take 'NNS' tagged tokens, because we're sure they are something
                    if tag in ['NNS']: 
                        # find the tag the NLTK NE tagger gave
                        if 'ORGANIZATION' in str(i):
                            named_entities.append([(token, tag, 'ORG')])
                        else:
                            named_entities.append([(token, tag, '-')])

    # print(named_entities)
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


def create_files(path, model, output_file='.ent.louis'):
    '''create the .ent files based on the model'''

    nlp = spacy.load(model)

    rawPathlist = glob.glob(path + '/en.raw')
    offsetPosList = glob.glob(path + '/en.tok.off.pos')

    for r, p in zip(rawPathlist, offsetPosList):


        # append lines from csv.reader to list, because can't iterate over csv.reader
        with open(p) as posFile:
            csvReader = csv.reader(posFile, delimiter=" ")
            lines = [line for line in csvReader]

        entities = []
        # create sentences w/ offsets in tuple
        sentData = create_sentences(r)
        # iterate over sentences
        for begin, end, sent in sentData:
            # create nlp pipeline
            doc = nlp(sent)
            # append entity offsets, text and tagged category
            for ent in doc.ents:
                # following entity labels are not used
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


            # lets try to find new entities with the NLTK NER tagger
            ne_chunk_input = []
            for line in lines:
                if int(line[1]) <= end:
                    ne_chunk_input.append((line[3], line[4]))
            named_entities_list = get_continuous_chunks(ne_chunk_input)
            ne_chunk_input = [] # return to empty input
            for item in named_entities_list:
                if len(item) == 1:
                    for ne in item:
                        # check if the NE from NLTK are already found by SpaCy
                        if any(ne[0] in ent[2] for ent in entities):
                            # NE found in entities, thus break loop
                            break
                        else:
                            # using enumerate to find lines after and before current 
                            for idx, line in enumerate(lines):
                                # check if NE matches token and it's POS tag also matches
                                if ne[0] == line[3] and ne[1] == line[4]:
                                    if ne[2] != '-':
                                        entities.append((line[0], line[1], ne[0], ne[2]))
                                    else:
                                        # hier nog iets doen?
                                        # TODO!!
                                        # print(line[0], line[1], ne[0], ne[2])
                                        entities.append((line[0], line[1], ne[0], ne[2]))


            # find 'ANI', 'SPO' and 'NAT' with WordNet
            categories = {'ANI': ['animal', 'bird'], 'SPO': ['sport'], 'NAT': ['ocean', 'river', 'mountain', 'crack', 'land']}
            for line in lines:
                token = line[3]
                tag = line[4]
                if tag in ['NNPS', 'NNS']:
                    synsets = wn.synsets(token, pos='n') # creates a list with all found synsets for noun
                    if len(synsets) > 0:
                        synset = wn.synsets(token, pos='n')[0] # only use the first synset found by WordNet
                        hypernyms = [i for i in synset.closure(lambda s:s.hypernyms())] 
                        for hyp in hypernyms:
                            if str(hyp) != "Synset('public_transport.n.01')": # door categorie 'sport' ging deze ook mee
                                for key, value_list in categories.items():  
                                    for cat in value_list:
                                        if cat in str(hyp):
                                            # check if the NE from NLTK are already found by SpaCy
                                            if any(token in ent[2] for ent in entities):
                                                break
                                            else:
                                                # komt bird etc er nu niet per bestand maar 1x in?
                                                # moeten kijken naar die loops...
                                                # want het moet natuurlijk per keer erin..
                                                entities.append((line[0], line[1], token, key))

        # iterate over both
        for ent in entities:
            for line in lines:
                # check if offsets of entity match ent.tok.off.pos token offsets
                if int(line[0]) == ent[0] and int(line[1]) == ent[1]:
                    # print(ent[2], ent[3])
                    line.append(ent[3])

        # with open(p + output_file, "w") as parserFile:
        #     for line in lines:
        #         item = ' '.join(line)
        #         parserFile.write("%s\n" %item)

        # print('Succesfully created "{0}" file in directory: {1}'.format(output_file, path))


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

    path = 'dev/*/*' # p36/d0690                      # set to 'dev/*/*' for all files
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
