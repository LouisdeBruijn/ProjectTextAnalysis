#!/usr/bin/python3
# File name: wikification.py
# Description: 
# Author: Louis de Bruijn
# Date: 11-06-2018

from __future__ import unicode_literals, print_function

import glob
import csv
import os
import collections
import nltk
import spacy
import plac
import random
from pprint import pprint 
from pathlib import Path
from spacy.util import minibatch, compounding
from collections import defaultdict

def main():
    
    rawPathlist = glob.glob('dev/p15/d0046/en.raw')
    goldPathList = glob.glob('dev/p15/d0046/en.tok.off.pos.ent')

    TRAIN_DATA = []

    # create training data
    for r, g in zip(rawPathlist, goldPathList):
        # create sentences w/ offsets
        sentData = []
        with open(r) as rawFile:
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
        

        # find annotated gold standard categories
        goldData = []
        with open(g) as goldFile:
            csvReader = csv.reader(goldFile, delimiter=" ")
            for line in csvReader:
                if len(line) > 5:
                    goldData.append(line)

        # combine to create training data
        for s in sentData:
            # create entity dictionary
            dic = defaultdict(list)
            # iterate through gold standard, find annotated tokens
            for g in goldData:
                # if the beginning ofset of token is in sentence ofsets
                if s[0] <= int(g[0]) <= s[1]:
                    # append all entities in one sentences to dic
                    # token offsets per document are coverted per sentence
                    dic['entities'].append((int(g[0])-s[0], int(g[1])-s[0], g[5])) # g[1] = doc offset, g[1]-s[0] = sentence offset
            if dic:
                TRAIN_DATA.append((s[2], dic))


    def train_model(model=None, output_dir=None, n_iter=100):
        """Load the model, set up the pipeline and train the entity recognizer."""
        if model is not None:
            nlp = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.blank("en")  # create blank Language class
            print("Created blank 'en' model")

        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = nlp.get_pipe("ner")

        # add labels
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
        with nlp.disable_pipes(*other_pipes):  # only train NER
            # reset and initialize the weights randomly – but only if we're
            # training a new model
            if model is None:
                nlp.begin_training()
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)

        # test the trained model
        for text, _ in TRAIN_DATA:
            doc = nlp(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

        # save model to output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            for text, _ in TRAIN_DATA:
                doc = nlp2(text)
                print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
                print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


    print(train_model(model=None, output_dir=None)) #output_dir=os.getcwd()

if __name__ == '__main__':
    main()
