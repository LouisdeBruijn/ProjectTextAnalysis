# Filename: Wikifier.py
# Description: Searches for a wikipedia page with tagged entities.
# Date: 15 juni 2018
# Author: F.R.P. Stolk

import wikipedia
import os
import glob
def read_files():
    cwd = os.getcwd()
    dirs = os.listdir('dev')
    offsetPosList = glob.glob('dev/*/*' + '/en.tok.off.pos.ent.louis')
    for x in offsetPosList:
            with open(x) as RawFile:
                file = RawFile.read()
                sentences = file.splitlines()
                entity = []
                word = []
                for x in sentences:
                    split_s = x.split()
                    if len(split_s) == 6:
                        print("test123" + split_s[3])
                        if len(entity) > 0:
                            if entity[len(entity)-1] == split_s[5]:
                                entity.append(split_s[5])
                                word.append(split_s[3])
                            else:
                                print(entity)
                                print(word)
                                entity = []
                                word = []
                                entity.append(split_s[5])
                                word.append(split_s[3])
                        else:
                            entity.append(split_s[5])
                            word.append(split_s[3])
                            print(entity)
                            print(word)
                    elif len(entity) > 0:
                        print(entity)
                        print(word)
                        entity = []
                        word = []



            #print(splitted_text)
def main():



    read_files()

if __name__ == '__main__':
    main()