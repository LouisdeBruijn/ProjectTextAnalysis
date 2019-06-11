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
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    return current_chunk



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

        i = 0 # counter
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
                    if ent.label_ == 'LOC': # Non-GPE locations, mountain ranges, bodies of water.
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
            sentence = []
            for line in lines:
                if int(line[1]) <= end:
                    sentence.append((line[3], line[4]))
            named_entities = get_continuous_chunks(sentence)
            sentence = [] # return to empty sentence
            for ne in named_entities:
                # check if the NE from NLTK are already found by SpaCy
                if any(ne in ent[2] for ent in entities):
                    break
                else:
                    # we moeten ook de offsets meegeven, dus dat proberen we zo!
                    for token in doc:
                        if ne == token.text:
                            # hier moeten we er dus een token aan geven
                            print("WE HAVE A WINNER")
                            entities.append(token.idx, i+token.idx, ne, '-')
               
            i += len(doc) # offset counter


        #### nadenken hoe we in godsnaam die nieuwe tags gaan geven.
        ### dat moet dus met wordnet.

        #### hier moeten we entities gaan toevoegen
        ### alleen weten we de offsets niet
        ## die moeten we op een of andere manier nog vinden

        ## stap 1 = nieuwe named entities vinden
        ## stap 2 = deze nieuwe entities classificeren
        ## sport en animal moeten we nog doen op basis van wn.synset.hypernym 


        # Wordnet operations.. ?..
        # for line in lines:
        #     if line[4] in ['NN', 'NNP', 'NNS', 'NNPS']:
        #         token = line[3]


        # iterate over both
        for ent in entities:
            for line in lines:
                # check if offsets of entity match ent.tok.off.pos token offsets
                if int(line[0]) == ent[0] and int(line[1]) == ent[1]:
                    print(ent[2], ent[3])
                    line.append(ent[3])

        with open(p + output_file, "w") as parserFile:
            for line in lines:
                item = ' '.join(line)
                parserFile.write("%s\n" %item)

        print('Succesfully created "{0}" file in directory: {1}'.format(output_file, path))


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

    path = 'dev/p36/d0690'                      # set to 'dev/*/*' for all files
    model = "en_core_web_sm"                    # SpaCy English model
    # model = os.getcwd() + '/spacy_model'        # our own model
    # model = os.getcwd() + '/spacy_modelv2'      # our own model + SpaCy English model
    output_file = '.ent.louis'                  # output file endings
    
    ## run it
    create_files(path, model, output_file)

    ## compare gold standard and parser files
    # print(compare(path, output_file))


if __name__ == '__main__':
    main()
