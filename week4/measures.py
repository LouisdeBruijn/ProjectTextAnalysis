#!/usr/bin/env python3
# File name: measures.py
# Description: script that does POS-tagging for files
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 14-05-2018

import glob
import csv
from collections import Counter
from collections import defaultdict
from nltk.metrics import ConfusionMatrix

def main():

    # create a dict w/ lists of annotations per file per annotator
    # path_list = glob.glob('group11/*/*/*.tok.off.pos.*')
    # annot = defaultdict(list)
    # for path in path_list:
    #     with open(path) as csv_file:
    #         annotations = []
    #         csv_reader = csv.reader(csv_file, delimiter=' ')
    #         for line in csv_reader:
    #             if len(line) > 5:
    #                 annotations.append(line[5])
    #         print(path, annotations)
    #         annot[path[:17]].append(annotations)



    # precision, recall and f-score for interisting entities vs non-interesting
    path_list = glob.glob('group11/*/*/*.tok.off.pos.l')
    louis = defaultdict(list)
    total = 0
    for path in path_list:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for line in csv_reader:
                if len(line) > 5:
                    louis[path[:17]].append((line[0], line[1], line[5]))
                total += 1

    path_list = glob.glob('group11/*/*/*.tok.off.pos.n')
    nick = defaultdict(list)
    for path in path_list:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for line in csv_reader:
                if len(line) > 5:
                    nick[path[:17]].append((line[0], line[1], line[5]))

    # initalize variables
    tp = fn = fp = 0

    for (k, v), (k2, v2) in zip(louis.items(), nick.items()):
        for i, i2 in zip(v, v2):
            if i[0] == i2[0] and i[1] == i2[1]:
                tp += 1
            else: 
                fn += 1
                fp += 1

    tn = total - tp


    precision = tp/(tp+fp)
    recall = tp/(tp+fn)

    print(precision, recall)


    #### original content ####
    ref  = 'DET NN VB DET JJ NN NN IN DET NN'.split()
    tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
    cm = ConfusionMatrix(ref, tagged)

    print(cm)

    labels = set('DET NN VB IN JJ'.split())

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

    print(true_positives)


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

