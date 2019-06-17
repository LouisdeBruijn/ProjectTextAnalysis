# Filename: Wikifier.py
# Description: Searches for a wikipedia page with tagged entities.
# Date: 15 juni 2018
# Author: F.R.P. Stolk

import wikipedia
import os
import glob
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
def read_files():
    cwd = os.getcwd()
    dirs = os.listdir('dev')
    offsetPosList = glob.glob('dev/*/*' + '/en.tok.off.pos.ent.louis')
    for x in offsetPosList:
            with open(x) as RawFile:
                new_file = []
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