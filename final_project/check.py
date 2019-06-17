#!/usr/bin/python3
# File name: check.py
# Description: Creates .ent files with annoted categories
# Author: Louis de Bruijn
# Date: 11-06-2018

import glob
import csv

def check():

    gold_tags = []
    parser_tags = []
    entity_missed = []
    entity_too_much = []
    path = 'dev/*/*'

    NORP_wrong = []
    NORP_right = []

    parser = glob.glob(path + '/en.tok.off.pos.ent.louis')
    gold = glob.glob(path + '/en.tok.off.pos.ent')

    for p, g in zip(parser, gold):
        # print(p, g)

        with open(g) as goldfile:
            goldLines = [line.rstrip().split() for line in goldfile]

        with open(p) as parserfile:
            parserLines = [line.rstrip().split() for line in parserfile]

        for line in goldLines:
            if len(line) > 5:
                gold_tags.append(line)

        for line in parserLines:
            if len(line) > 5:
                parser_tags.append(line)


        for p, g in zip(parserLines, goldLines):
            if len(p) > 5 and len(g) < 6:
                entity_too_much.append((p, g))
            elif len(p) < 6 and len(g) > 5:
                entity_missed.append((p, g))



            if len(p) > 5:
                if p[5] == 'EXTRA' and len(g) < 6 :
                    NORP_wrong.append((p, g))
                elif p[5] == 'EXTRA' and len(g) > 5 :
                    NORP_right.append((p,g))

    print('NORP wrong', len(NORP_wrong))
    print('NORP right', len(NORP_right))

    for i in NORP_right:
        print(i)
    print()
    for i in NORP_wrong:
        print(i)

    print()         

    # for i in entity_too_much:
    #     print(i)

    print(len(gold_tags)) # all gold tagged entities
    print(len(parser_tags)) # all parser tagged entities
    print(len(entity_missed)) # parser did not tag entity when it actually is
    print(len(entity_too_much)) # parser tagged an entity, when it is not            



def main():

    err1 = [] # met SpaCy NORP als 'EXTRA'
    err2 = [] # SpaCy model
    err3 = [] # SpaCy + own model
    err4 = [] # own model

    with open('errors2.txt') as error2:
        for line in error2:
            err2.append(line)

    with open('errors3.txt') as error3:
        for line in error3:
            err3.append(line)

    with open('errors4.txt') as error4:
        for line in error4:
        err4.append(line)


    print('SpaCy model', len(err2))
    print('SpaCy + own model', len(err3))
    print('own model', len(err4))

    # for e1, e2 in zip(err2, err3):


if __name__ == '__main__':
    main()