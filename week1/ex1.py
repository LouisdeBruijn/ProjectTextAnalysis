#!/usr/bin/env python3
# File name: ex1.py
# Description: script that generates all the information required in exercise 1
# Author: Louis de Bruijn
# Date: 23-04-2018

import nltk # v3.4

def main():
    # tell Python we want to use the Gutenberg corpus
    from nltk.corpus import gutenberg

    # which files are in this corpus?
    print(gutenberg.fileids())

    # get the raw text of a corpus = one string
    senseText = gutenberg.raw("austen-sense.txt")

    # print the first 317 characters of the text
    senseText[:317]

    # get the words of a corpus as a list
    senseWords = gutenberg.words("austen-sense.txt")
    # print the first 20 words
    print(senseWords[:20])

    # get the sentences of a corpus as a list of lists
    # (one list of words per sentence)
    senseSents = gutenberg.sents("austen-sense.txt")

    # print out the first four sentences
    print(senseSents[:4])

        # Read the text (as we know it already)
    path = "holmes.txt"
    f = open(path)
    rawText = f.read()
    f.close()
    print(rawText[:165])

    # Split the text up into sentences
    """ sent_tokenize calls the NLTK's currently
    recommended sentence tokenizer to tokenize sentences
    in the given text. Currently, this uses
    PunktSentenceTokenizer.
    """
    sents = nltk.sent_tokenize(rawText)
    print(sents[20:22])

    # Tokenize the sentences using nltk
    """ Use NLTK's currently recommended word
    tokenizer to tokenize words in the given sentence.
    Currently, this uses TreebankWordTokenizer.
    This tokenizer should be fed a single sentence at a time.
    """
    tokens = []
    for sent in sents:
        tokens += nltk.word_tokenize(sent)
    print(tokens[300:350])

    # bigrams() function
    sent = ['The', 'cat', 'that', 'sat', 'on', 'the', 'mat', 'also', 'sat', 'on', 'the', 'sofa']
    list(nltk.bigrams(sent))

    # frequencies for bigrams
    bigrams = nltk.bigrams(sent)
    fdist = nltk.FreqDist(bigrams)
    for b, f in fdist.items():
        print(b, f)


if __name__ == '__main__':
    main()

