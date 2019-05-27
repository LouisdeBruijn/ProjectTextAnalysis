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
    path_list = [files for files in glob.glob('group11/*/*/*.tok.off.pos.l')]
    louis = []
    for file in path_list:
        with open(file) as f:
            text = f.readlines()
            print(len(text), file)
        for line in text:
            line = line.split()
            if len(line) == 7:
                louis.append(line[5])
            else:
                louis.append("NONE")

    path_list = [files for files in glob.glob('group11/*/*/*.tok.off.pos.n')]
    nick = []
    for file in path_list:
        with open(file) as f:
            text = f.readlines()
            print(len(text), file)
        for line in text:
            line = line.split()
            if len(line) == 7:
                nick.append(line[5])
            else:
                nick.append("NONE")
    path_list = glob.glob('group11/*/*/*.tok.off.pos.l')
    friso = defaultdict(list)
    for path in path_list:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for line in csv_reader:
                if len(line) > 5:
                    friso[path[:17]].append((line[0], line[1], line[5]))
    # initalize variables
    tp = fn = fp = 0

# Nick and Louis comparison
    cm = ConfusionMatrix(nick, louis)
    print(cm)
    labels = set(nick + louis)
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

# Nick and Friso comparison
  
if __name__ == '__main__':
    main()

