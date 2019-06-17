#!/usr/bin/python3
# File name: check.py
# Description: check w/ measures.py TP/FP/TN/FN and F1-score
# Author: Louis de Bruijn
# Date: 11-06-2018

import glob
from collections import Counter
from nltk.metrics import ConfusionMatrix


def main():
    '''compares all of the parser and gold-standard files'''
    path = 'dev/*/*'
    parser = glob.glob(path + '/en.tok.off.pos.ent.dev2')
    gold = glob.glob(path + '/en.tok.off.pos.ent')

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


if __name__ == '__main__':
    main()