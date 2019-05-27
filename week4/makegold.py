#!/usr/bin/env python3
# File name: pos_tag.py
# Description: script that does POS-tagging for files
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 14-05-2018

import glob
import csv
import sys


def main(argv):
    path_list = glob.glob('group11/*/*/*.tok.off.pos')
    print(path_list)
    for path in path_list:
        print(path)
        with open(path+".l") as l, open(path+".f") as f, open(path+".n.nodash") as n:
            #csv_reader = csv.reader(csv_file, delimiter=' ')
            #for line in csv_reader:
            #    print(line)
            rawText_n = n.read()
            rawText_f = f.read()
            rawText_l = l.read()

            sents_n = rawText_n.split('\n') # tokenize rawText to sentences
            sents_f = rawText_f.split('\n') # tokenize rawText to sentences
            sents_l = rawText_l.split('\n') # tokenize rawText to sentences
            sents_n.pop() # remove useless newline at end of every file
            sents_f.pop() # remove useless newline at end of every file
            sents_l.pop() # remove useless newline at end of every file

            for i in range(len(sents_n)):
                n_sent = sents_n[i].split()
                f_sent = sents_f[i].split()
                l_sent = sents_l[i].split()
                if not(n_sent == f_sent and f_sent == l_sent):
                    print("n: ")
                    print(n_sent)
                    print("f: ")
                    print(f_sent)
                    print("l: ")
                    print(l_sent)
                    inp = input()
                    if inp == "f":
                        sents_n[i] = sents_f[i]
                    elif inp == "l":
                        sents_n[i] = sents_l[i]
                    elif inp != "n":
                        print("ERROR BUDDY, picking N")
            
            out_text = "\n".join(sents_n)

            f = open(path + ".ent", "w")
            print(out_text, file = f)


if __name__ == "__main__":
    main(sys.argv)