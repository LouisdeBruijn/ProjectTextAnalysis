#!/usr/bin/env python3
# File name: pos_tag.py
# Description: script that does POS-tagging for files
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 14-05-2018

import glob
import csv
import sys


def main(argv):
    path_list = glob.glob('group11/*/*/*.tok.off.pos.' + argv[1])
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

            for i in range(len(sents)):
                spl_sent = sents[i].split()
                if len(spl_sent) > 5 and spl_sent[5] == 'PERSON':
                    print("found one")
                    spl_sent[5] = 'PER'
                    sents[i] = " ".join(spl_sent)
            
            out_text = "\n".join(sents)

            f = open(path, "w")
            print(out_text, file = f)


if __name__ == "__main__":
    main(sys.argv)