# README #

This README describes the files in this directory and the necessary steps to get oyr Wikification application up and running. This Wikifaction system makes use of four ner taggers to find named entities in documents and classify them in eight different categories. 

### NER taggers used ###

- Stanford NLP ner tagger
- Wordnet ner tagger through hypernyms
- NLTK ner tagger
- SpaCy ner tagger

### Named Entity tags ###
 - COU: all country names and state names. Ex: Alaska, Burkina Faso.
 - CIT: all cities and smaller towns. Ex: Rome, Groningen.
 - NAT: natural places. Ex: Mississipi River, Springsteen.
 - PER: persons, limited to proper nouns. Ex: Bill Clinton, Johnny Dep.
 - ORG: organisations and companies. Ex: Apple, ONU.
 - ANI: animals. Ex: rabbits, goose.
 - SPO: sports. Ex: football, baseball.
 - ENT: entertainment. Ex: books, songs, films.

### Dependencies and files ###
- GPE/countries.txt: to find countries
- GPE/cities.txt: to find cities
- stanford-corenlp-full-2018-10-05/* for Stanford NLP parser with specified server settings.


# Files and imported libraries #

## Program files ##

$python3 create_files.py -- annotate tokens with entity tags and create .ent.dev files
$python3 train_model -- trains a SpaCy model on the development data
$python3 measures.py -- create a Confusion matrix and F1 scores per category tag
$python3 wikifier.py -- annotate entities with Wikipedia links and create .ent.wiki files

## Standard Python libraries ##
Python 3.7.1 (including glob, os and collections)
csv 1.0

## Imported libraries ##

### PyWSD ###
description: multiple Lesk algorithms to disambiguate WordNet synsets
installation: $pip install -U pywsd
PyWSD 1.2.1

### SpaCy ###
description: an open-source software library for advanced Natural Language Processing pipeline
installation: $pip install -U spacy
Spacy 2.1.3

### NLTK ###
description: a leading platform for building Python programs to work with human language data
installation: pip install --user -U nltk
NLTK 3.4.3

### Stanford NLP tagger ###
The following files are needed to instal the Stanford NLP tagger:
- stanford-corenlp-full-2018-10-05.zip 
- server.properties

The server.properties are to be included in the directory where the stanford-corenlp is located and the following command to be run:

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties server.properties -preload tokenize,ssplit,pos,lemma,ner,parse,depparse -status_port 9000 -port 9000 -timeout 15000 &


# PTA #

This directory includes all of our work for the Project Text Analysis final project of Group 11.

## who did what
## Friso
Wikification of entities
## Louis
SpaCy, NLTK and WordNet ner tagger, pipeline, data pre-processing
## Nick
Stanford NLP tagger and WordNet tagger
