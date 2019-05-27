#!/usr/bin/env python3
# File name: gold_standard.py
# Description: script that creates a gold-standard
# Author: Louis de Bruijn & Friso Stolk & Nick Algra
# Date: 27-05-2018

import os
import glob
import csv
from collections import defaultdict
from collections import Counter

def main():


    path_list = glob.glob('group11/*/*/')
    for path in path_list:
        annotations = defaultdict(list)
        for filename in os.listdir(path):
            if filename.endswith("pos.l") or filename.endswith('pos.n') or filename.endswith('pos.f'):
                with open(path+filename) as f:
                    csv_reader = csv.reader(f, delimiter=' ')
                    for line in csv_reader:
                        if len(line) > 5:
                            annotations[line[2]].append(line[5])
        
        gold_standard = {}
        # print(path+filename)
        for key, value in annotations.items():
            # print(key, value)
            counter = {}
            for v in value:
                counter[v] = counter.get(v, 0) +1
            # print(counter)
            for cat, count in counter.items():
                if count == 3 or count == 2:
                    gold_standard[key] = cat
                elif count == 1:
                    print(cat, count)
        
        print(gold_standard)



if __name__ == '__main__':
    main()

