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

def main():
	# Opdracht 1
	tokens = nltk.word_tokenize("Peter really liked the movies and warm pop-corn . He would never bring Mira with him, though .")
	print(tokens)
	print(nltk.corpus.brown.tagged_words(tagset='universal'))
	# Opdracht 2
	br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
	br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')
	print(br_tw)
	print(br_ts)
if __name__ == "__main__":
	main()