# Filename: Wikifier.py
# Description: Searches for a wikipedia page with tagged entities.
# Date: 15 juni 2018
# Author: F.R.P. Stolk

import wikipedia
import os
import glob
def check_next(x,splitted_text, entity):
    if len(splitted_text[x+1].split()) == 6:
        if splitted_text[x+1].split()[5] == splitted_text[x].split()[5]:
            entity.append(splitted_text[x+1].split()[3])
            x+=1
            check_next(x,splitted_text,entity)
    else:
        print(entity)
def read_files():
    cwd = os.getcwd()
    dirs = os.listdir('dev')
    offsetPosList = glob.glob('dev/*/*' + '/en.tok.off.pos.ent.louis')
    entities = []
    for x in offsetPosList:
        with open(x) as posFile:
            rawText = posFile.read()
            splitted_text = rawText.splitlines()
            #print(splitted_text)
            entity = []
            for i in range(len(splitted_text)):
                words = splitted_text[i].split()
                if len(words) == 6:
                    print(splitted_text[i].split()[5])
                    entity.append(words[3])
                    print(check_next(i, splitted_text, entity))
                    try:
                        page = wikipedia.page(words[3])
                        URL = page.url
                        #print(URL)
                    except wikipedia.exceptions.DisambiguationError as e:
                        x = 1
                entity = []
def main():



    read_files()

if __name__ == '__main__':
    main()