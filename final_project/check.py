#!/usr/bin/python3
# File name: check.py
# Description: check F1-scores and confusion matrix for entity tags and accuracy scores for Wikilinks
# Author: Louis de Bruijn
# Date: 11-06-2018

import glob
from collections import Counter
from nltk.metrics import ConfusionMatrix


def measures_entity(path, parser_filename, gold_filename):
    '''compares all of the entities in the parser and gold-standard files'''
    parserLines = []
    goldLines = []

    for p, g in zip(parser, gold):
        # print(p, g)

        with open(p) as parserFile:
            for line in parserFile:
                # remove newline character and split in list items
                line = line.rstrip().split()
                # remove the offsets per line
                parserLines.append(line[2:])
                    
        with open(g) as goldFile:
            for line in goldFile:
                # remove newline character and split in list items
                line = line.rstrip().split()
                # remove the offsets per line
                goldLines.append(line[2:])

    parserTags = []
    goldTags = []

    labels = set()

    for line in parserLines:
        if len(line) > 3:
            parserTags.append(line[3])
            labels.add(line[3])
        else:
            parserTags.append(" ")

    for line in goldLines:
        if len(line) > 3:
            labels.add(line[3])
            goldTags.append(line[3])
        else:
            goldTags.append(" ")

    gold = goldTags
    parser = parserTags

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


def accuracy_wikilinks():
    '''computes the accuracy score for the wikilinks'''
    parserLines = []
    goldLines = []

    for p, g in zip(parser, gold):
        # print(p, g)

        with open(p) as parserFile:
            for line in parserFile:
                # remove newline character and split in list items
                line = line.rstrip().split()
                # remove the offsets per line
                parserLines.append(line[2:])
                    
        with open(g) as goldFile:
            for line in goldFile:
                # remove newline character and split in list items
                line = line.rstrip().split()
                # remove the offsets per line
                goldLines.append(line[2:])


    for x, y in zip(parserLines, goldLines):
        print(x, y)
        exit()



    parserLinks = []
    goldLinks = []

    ## accuracy = correct links / total links 
    # total links = all the times where both parser and gold have a link
    for p_line, g_line in zip(parserLines, goldLines):
        if len(p_line) > 4 and len(g_line) > 4:
            parserLinks.append(line[4])
            goldLinks.append(line[4])


    acc = 0
    total = len(goldLinks)
    for p_link, g_link in zip(parserLinks, goldLinks):
        if p_link == g_link:
            acc += 1

    print('accuracy score:')
    print(acc/total)


def main():
    path = 'test/*/*'
    parser = glob.glob(path + '/en.tok.off.pos.ent.test1')
    gold = glob.glob(path + '/en.tok.off.pos.ent')

    ## compare the entity tags of parser and gold
    measures_entity(path, parser, gold)

    ## get accuracy scores for the Wikilinks
    accuracy_wikilinks(path, parser, gold)

if __name__ == '__main__':
    main()