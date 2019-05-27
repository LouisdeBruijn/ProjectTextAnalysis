#!/usr/bin/env python3
# File name: pos_tag.py
# Description: script that does POS-tagging for files
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 14-05-2018

import nltk
import glob
import csv


def main():
    path_list = glob.glob('group11/*/*/*.tok.off')
    print(path_list)
    for path in path_list:
        print(path)
        with open(path) as f:
            #csv_reader = csv.reader(csv_file, delimiter=' ')
            #for line in csv_reader:
            #    print(line)
            rawText = f.read()

            sents = rawText.split('\n') # tokenize rawText to sentences
            sents.pop() # remove useless newline at end of every file

            tokens = [sent.split()[3] for sent in sents]
            pos_tokens = nltk.pos_tag(tokens)
            for i in range(len(sents)):
                sents[i] += " " + pos_tokens[i][1]
            out_text = "\n".join(sents)

            f = open(path + ".pos", "w")
            print(out_text, file = f)


if __name__ == "__main__":
    main()