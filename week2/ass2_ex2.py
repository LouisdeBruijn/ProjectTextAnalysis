# Filename: ass2_ex2.py
# Description: Opdracht2 van week 2
# Authors: Friso Stolk & Louis de Bruijn
# Date: 06 May 2019

import nltk
from nltk.tokenize import RegexpTokenizer # tokanizer zonder punctation.
import operator

def main():

    # kan dit weg?
    # Opdracht 1
    # tokens = nltk.word_tokenize("Peter really liked the movies and warm pop-corn . He would never bring Mira with him, though .")
    # print(tokens)
    # print(nltk.corpus.brown.tagged_words(tagset='universal'))

    # Opdracht 2
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')

    print("### Exercise 2a: amount of words and sentences")
    print('sentences:', len(br_tw))
    print('words:', len(br_ts))

    print("### Exercise 2b: 50th and 75th word and POS-tag")
    print("50th word '{0}' and POS-tag '{1}'".format(br_tw[50][0], br_tw[50][1]))
    print("75th word '{0}' and POS-tag '{1}'".format(br_tw[75][0], br_tw[75][1]))

    print("### Exercise 2c: amount of different POS-tags in Brown category")
    # Finding the not duplicates part of speech
    not_duplicates = [x[1] for x in br_tw]
    print("There are {0} different POS-tags in Brown category.".format(len(set(not_duplicates))))

    print("### Exercise 2d: top 15 words and counts")
    all_words = [x[0] for x in br_tw]
    print(nltk.FreqDist(all_words).most_common(15))

    print("### Exercise 2e: top 15 POS-tags and counts")
    all_words = [x[1] for x in br_tw]
    print(nltk.FreqDist(all_words).most_common(15))

    print("### Exercise 2f: the most frequent POS-tags in sentence X")
    # excersize f just change 20 to 40 if you want to know the other one.
    allwords = [x[0] for x in br_ts[60]]
    print(nltk.FreqDist(allwords).most_common(15))
    # dit klopt volgens mij niet

    print("### Exercise 2g: most frequent adverb")
    allwords2 = [x for x in br_tw if x[1] == "RB"]
    print(nltk.FreqDist(allwords2).most_common(1))

    print("### Exercise 2h: most frequent adjective")
    allwords3 = [x for x in br_tw if x[1] == "JJ"]
    print(nltk.FreqDist(allwords3).most_common(1))

    print("### Exercise 2i: three distinct POS-tags for word 'so' are")
    # excersize i and j: the word so and his part of speech
    allwords = [x for x in br_tw if x[0] == "so"]
    all_words = nltk.ConditionalFreqDist(br_tw)
    for item in all_words["so"].most_common():
        print(item[0])

    print("### Exercise 2j: the most frequent POS-tag for the word 'so' is")
    print("The POS-tag {0} and its count {1}".format(all_words["so"].most_common(1)[0][0], all_words["so"].most_common(1)[0][1]))
   
    print("### Exercise 2k: example sentences with POS-tags for word 'so' ")
    allwords = [x for x in br_ts for i in x if i[0]=="so"]
    example1 = [x for x in allwords for i in x if i[0] == "so" and i[1] =="QL"]
    example2 = [x for x in allwords for i in x if i[0] == "so" and i[1] =="RB"]
    example3 = [x for x in allwords for i in x if i[0] == "so" and i[1] =="CS"]
    for i in range(len(example1[0])):
        print(example1[0][i][0], end=" ")
    print()
    for i in range(len(example2[0])):
        print(example2[0][i][0], end=" ")
    print()
    for i in range(len(example3[0])):
        print(example3[0][i][0], end=" ")
    print()
    print("### Exercise 2l: ")
    tags_after = [b[1] for (a,b) in nltk.bigrams(br_tw) if a[0] == 'so']
    after_most = nltk.FreqDist(tags_after)
    for tag, freq in after_most.most_common(1):
        print(tag, freq)
    tags_before = [a[1] for (a,b) in nltk.bigrams(br_tw) if b[0] == 'so']
    before_most = nltk.FreqDist(tags_before)
    for tag, freq in before_most.most_common(1):
        print(tag, freq)
    """ Excersize 3 """
    path = "holmes.txt"
    f = open(path)
    rawText = f.read()
    f.close()
    pos_tag = nltk.pos_tag(nltk.word_tokenize(rawText))
    #print(pos_tag)
    """ Excersize 4 """
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bifinder = nltk.BigramCollocationFinder.from_words(pos_tag)
    best = bifinder.nbest(bigram_measures.pmi, 5)
    print(best)
if __name__ == "__main__":
	main()