# Filename: Wikifier.py
# Description: Searches for a wikipedia page with tagged entities.
# Date: 15 juni 2018
# Author: F.R.P. Stolk

import wikipedia
import os
import glob
from collections import defaultdict

def find_wiki(entity, cat):


        try:
            # print(entity, cat)
            page = wikipedia.page(entity)
            URL = page.url
            #print(entity, URL)
            return URL
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            if  cat == "COU":
                keywords = ["culture", "province"]
            elif cat == "CIT":
                keywords = []
            elif cat == "NAT":
                keywords = ["river", "mountain"]
            elif cat == "PER":
                keywords = ["name", "given name", "surname", "person"]
            elif cat == "ORG":
                keywords = []
            elif cat == "ANI":
                keywords = []
            elif entity == "SPO":
                keywords = []
            elif cat == "ENT":
                keywords = ["book", "story", "novel", "song", "album", "magazine", "game", "party", "episode", "series", "film"]
            for option in options:
                for keyword in keywords:
                    if keyword in option:
                        page = wikipedia.page(option)
                        URL = page.url
                        return URL
                if keywords not in options:
                    URL = '-'
                    return URL
        except wikipedia.exceptions.PageError as f:
            print(f)


def check_next(lines, idx, entities):

    identifier = next(lines)
    if len(identifier) > 5:
        for key in entities.keys():
            if identifier[5] == key:
                entities[identifier[5]].append(identifier[3])
                idx += 1
                return check_next(lines, idx, entities)
            # als de volgende line een andere CAT heeft    
            else:
                return entities
    else:
        return entities






def read_files():

    offsetPosList = glob.glob('dev/*/*' + '/en.tok.off.pos.ent.louis')

    # door files itereren
    for path in offsetPosList:
        print(path)

        with open(path) as file:
            lines = [line.rstrip().split() for line in file]

        # iterable object
        lines = iter(lines)
        # create wikilinks w/ tuple (index, link)
        wikilinks = []

        # create index
        idx = 0
        # lets go
        try:
            for line in lines:
                idx += 1
                entities = defaultdict(list)
                if len(line) > 5:
                    entities[line[5]].append(line[3])
                    entities = check_next(lines, idx, entities)

                    for key, value in entities.items():
                        if len(value) > 1:
                            for i, v in enumerate(value):
                                wikilinks.append((idx+i, find_wiki(' '.join(value), key)))
                        else:
                            wikilinks.append((idx, find_wiki(' '.join(value), key)))

                    for i in entities.values():
                        idx += len(i)

        
        except StopIteration:
            continue


        with open(path) as file:
            lines = [line.rstrip().split() for line in file]

        for index, line in enumerate(lines):
            for item in wikilinks:
                if index == item[0]-1:
                    line.append(item[1])


        with open(path + '.wiki', "w") as parserFile:
            for line in lines:
                item = ' '.join(line)
                parserFile.write("%s\n" %item)
    






    # cwd = os.getcwd()
    # dirs = os.listdir('dev')
    # offsetPosList = glob.glob('dev2/*/*' + '/en.tok.off.pos.ent.louis')
    # for x in offsetPosList:
    #         with open(x) as RawFile:
    #             new_file = []
    #             file = RawFile.read()
    #             sentences = file.splitlines()
    #             entity = []
    #             word = []
    #             for x in sentences:
    #                 split_s = x.split()
    #                 if len(split_s) == 6:
    #                     if len(entity) > 0:
    #                         if entity[len(entity)-1] == split_s[5]:
    #                             entity.append(split_s[5])
    #                             word.append(split_s[3])
    #                         else:
    #                             split_s.append(find_wiki(word,entity))
    #                             new_file.append(find_wiki(word,entity))
    #                             entity = []
    #                             word = []
    #                             entity.append(split_s[5])
    #                             word.append(split_s[3])
    #                     else:
    #                         entity.append(split_s[5])
    #                         word.append(split_s[3])
    #                         new_file.append(find_wiki(word,entity))
    #                 elif len(entity) > 0:
    #                     new_file.append(find_wiki(word,entity))
    #                     entity = []
    #                     word = []
    #                 else:
    #                     new_file.append(x)
    #             for i in new_file:
    #                 print(i)



            #print(splitted_text)
def main():



    read_files()

if __name__ == '__main__':
    main()