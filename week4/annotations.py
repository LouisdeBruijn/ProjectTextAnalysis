#!/usr/bin/env python3
# File name: annotations.py
# Description: 
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 25-05-2018

import glob
import csv


def main():

    path_list = glob.glob('group11/*/*/*.tok.off.pos.l')
    for path in path_list:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for line in csv_reader:
                if len(line) == 6: # no entity class tag ?
                    print(path, line)
                elif len(line) == 7:
                    # print(path[:17], line[5], line[6]) # check correctness
                    if ' ' in line[6]:
                        print(line[6]) # whitespaces in link
                    elif ' ' in line[5]:
                        print(line[5]) # whitespaces in entiy class tag
                    elif line[6] == '-':
                        print(path, line)
                    elif line[6] == 'Washington': # could link to the disambiguation page
                        print(line)



if __name__ == '__main__':
    main()
