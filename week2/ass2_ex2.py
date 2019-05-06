# Filename: ass2_ex2.py
# Description: Opdracht2 van week 2
# Authors: Friso Stolk & Louis de Bruijn
# Date: 4 May 2019
"""
Penn treebank POS tagging
    Peter = NN
    really = RB
    liked = VBD
    the = DT
    movies = NNPS
    and = CC
    warm = JJ
    pop-corn = NN
    . = .
    He = PRP
    would = VB
    never = RB
    bring = VB
    Mira = NN
    with = JJ
    him = NNP
    , = :
    though = CC
    
    
    
    Brown
    Peter = NN
    really = ADV
    liked = BEDZ
    the = IN
    movies = NN
    and = ABX
    warm = JJ
    pop-corn = NN
    . = sentence
    He = DT
    would = HV
    never = ADV
    bring = BEZ
    Mira = NN
    with = ABN
    him = DT
    , = comma
    though = 
    
    
    
    
    NLTK Universal tagset
    Peter = Noun
    really = adv
    liked = Verb
    the = det
    movies = noun
    and = conj
    warm = adj
    pop-corn = noun
    . = punctuation
    He = pronoun
    would = verb
    never = adv
    bring = verb
    Mira = noun
    with = det
    him = pronoun
    , =  punctuation
    though = det

"""
import nltk
from nltk.tokenize import RegexpTokenizer # tokanizer zonder punctation.
import operator

def main():
    # Opdracht 1
    tokens = nltk.word_tokenize("Peter really liked the movies and warm pop-corn . He would never bring Mira with him, though .")
    print(tokens)
    print(nltk.corpus.brown.tagged_words(tagset='universal'))
    # Opdracht 2
    br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
    br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')
    print(len(br_tw))
    print(len(br_ts))
    print(br_tw[50])
    print(br_tw[75])
    print(len(set(br_tw)))

	# Finding the not duplicates part of speech
    not_duplicates = [x[1] for x in br_tw]
    print(len(set(not_duplicates)))

    # Looking top 15 words
    all_words = [x[0] for x in br_tw]
    print(nltk.FreqDist(all_words).most_common(15))
    # excersize f just change 20 to 40 if you want to know the other one.
    allwords = [x[0] for x in br_ts[60]]
    print(nltk.FreqDist(allwords).most_common(1))
    # excersize g: most common adverb
    allwords2 = [x for x in br_tw if x[1] == "RB"]
    print(nltk.FreqDist(allwords2).most_common(1))
    # excersize h: most frequent adjective
    allwords3 = [x for x in br_tw if x[1] == "JJ"]
    print(nltk.FreqDist(allwords3).most_common(1))
    # excersize i and j: the word so and his part of speech
    allwords = [x for x in br_tw if x[0] == "so"]
    print(nltk.FreqDist(allwords).most_common(5))
    all_words = nltk.ConditionalFreqDist(br_tw)
    print(all_words["so"].most_common())
    print(all_words["so"].most_common(1))

    """ Excersize 3 """
    path = "holmes.txt"
    f = open(path)
    rawText = f.read()
    f.close()
    pos_tag = nltk.pos_tag(nltk.word_tokenize(rawText))
    #print(pos_tag)

if __name__ == "__main__":
	main()