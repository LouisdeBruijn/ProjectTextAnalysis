# Filename: Wikifier.py
# Description: Searches for a wikipedia page with tagged entities.
# Date: 15 juni 2018
# Author: F.R.P. Stolk

import wikipedia
import os
import glob
from itertools import cycle


def find_wiki(word, entity):
    entity = entity[0]
    if len(word) > 1:
        whole_word = ''
        whole_word = " ".join(word)
        try:
            page = wikipedia.page(whole_word)
            URL = page.url
            print(word, entity)
            return URL
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            if  entity == "country" or "state" or "LOCATION":
                keywords = ["culture", "province"]
            elif entity == "city" or "town":
                keywords = []
            elif entity == "natural places":
                keywords = ["river", "mountain"]
            elif entity == "person":
                keywords = ["name", "given name", "surname", "person"]
            elif entity == "organization":
                keywords = []
            elif entity == "animal":
                keywords = []
            elif entity == "sport":
                keywords = []
            elif entity == "entertainment":
                keywords = ["book", "story", "novel", "song", "album", "magazine", "game", "party", "episode", "series", "film"]
            for option in options:
                for keyword in keywords:
                    if keyword in option:
                        page = wikipedia.page(option)
                        URL = page.url
                        print(word)
                        return URL
                if keywords not in options:
                    page = wikipedia.page(options[0])
                    URL = page.url
                    return URL
        except wikipedia.exceptions.PageError as f:
            print(f)
    return '-'


def read_files():


    offsetPosList = glob.glob('dev/*/*' + '/en.tok.off.pos.ent')
    print(offsetPosList)
    exit()

    # door ifles itereren
    for path in offsetPosList:
        # maak list met lines
        lines = []
        with open(path) as file:
            lines = [line.rstrip().split() for line in file]

        # 
        for idx, line in enumerate(lines):
            if len(line) > 5:

                ## wikify 
                lines[idx+1]

                line = line + wiki_url

        with open(path + '.wiki', "w") as parserFile:
            for line in lines:
                item = ' '.join(line)
                parserFile.write("%s\n" %item)






            file = RawFile.read()
            sentences = file.splitlines()
            entity = []
            word = []
            for x in sentences:
                split_s = x.split()
                if len(split_s) == 6:
                    if len(entity) > 0:
                        if entity[len(entity)-1] == split_s[5]:
                            entity.append(split_s[5])
                            word.append(split_s[3])
                        else:
                            print(find_wiki(word,entity))
                            new_file.append(" ".join(split_s))
                            entity = []
                            word = []
                            entity.append(split_s[5])
                            word.append(split_s[3])
                    else:
                        entity.append(split_s[5])
                        word.append(split_s[3])
                        new_file.append(find_wiki(word,entity))
                elif len(entity) > 0:
                    new_file.append(find_wiki(word,entity))
                    entity = []
                    word = []
                else:
                    new_file.append(x)
            for i in new_file:
                print(i)



            #print(splitted_text)
def main():



    read_files()

if __name__ == '__main__':
    main()