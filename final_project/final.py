import glob
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.parse import CoreNLPParser


def hypernym_of(synset1, synset2):
    """ Returns True if synset2 is a hypernym of 
    synset1, or if they are the same synset. 
    Returns False otherwise. """
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym: 
            return True
        if hypernym_of(hypernym, synset2): 
            return True
    for inst_hypernym in synset1.instance_hypernyms():
        if synset2 == inst_hypernym: 
            return True
        if hypernym_of(inst_hypernym, synset2): 
            return True
    return False


def tag_named_entities(tokens):
    return nec_tokens


def main():
    path_list = glob.glob('dev/*/*/*.tok.off.pos')
    print(path_list)
    for path in path_list:
        print(path)
        with open(path) as f:
            ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
            rawText = f.read()

            sents = rawText.split('\n') # tokenize rawText to sentences
            sents.pop() # remove useless newline at end of every file
            tokens = [sent.split()[3] for sent in sents]
            nec_tokens = ner_tagger.tag(tokens)
            #print("Tokens: {}".format(len(tokens)))
            #print("NEC: {}".format(len(nec_tokens)))
            j = 0
            for i in range(len(tokens)):
                token = nec_tokens[j][0]
                token = token.replace('`', "'")
                token = token.replace('-LRB-', '(')
                token = token.replace('-RRB-', ')')
                token = token.replace("''", '"')
                while token != tokens[i]:
                    #print("Merging tokens!")
                    j += 1
                    token += nec_tokens[j][0]
                    token = token.replace('`', "'")
                    token = token.replace('LBR', '(')
                    token = token.replace('RBR', ')')
                    token = token.replace("''", '"')
                    #print(tokens[i])
                    #print(token)
                    #print(token == tokens[i])
                #print(token)
                #print(tokens[i])
                nec = nec_tokens[j][1]
                #if nec != 'O':
                #    print(token)
                #    print(nec)
                pos = sents[i].split()[4]
                if nec == 'PERSON':
                    sents[i] += ' PER'
                elif nec == 'ORGANIZATION':
                    sents[i] += ' ORG'
                elif nec == 'COUNTRY' or nec == 'STATE_OR_PROVINCE':
                    sents[i] += ' COU'
                elif nec == 'CITY':
                    sents[i] += ' CIT'
                elif nec == 'LOCATION':
                    lesk_synset = lesk(tokens, token, 'n')
                    if lesk_synset and (hypernym_of(lesk_synset, wn.synset('country.n.02')) or hypernym_of(lesk_synset, wn.synset('state.n.01'))):
                        sents[i] += ' COU'
                    elif lesk_synset and (hypernym_of(lesk_synset, wn.synset('city.n.01')) or hypernym_of(lesk_synset, wn.synset('town.n.01'))):
                        sents[i] += ' CIT'
                    else:
                        sents[i] += ' NAT'
                elif pos == 'NN' or pos == 'NNS':
                    lesk_synset = lesk(tokens, token, 'n')
                    if lesk_synset and hypernym_of(lesk_synset, wn.synset('animal.n.01')):
                        sents[i] += ' ANI'
                    elif lesk_synset and hypernym_of(lesk_synset, wn.synset('sport.n.01')):
                        sents[i] += ' SPO'
                elif (pos == 'NNP' or pos == 'NNPS') and not lesk(tokens, token):
                    sents[i] += ' ENT'
                j += 1
                    
            
            #pos_tokens = nltk.pos_tag(tokens)
            #for i in range(len(sents)):
            #    sents[i] += " " + pos_tokens[i][1]
            out_text = "\n".join(sents)

            f = open(path + ".wncorenlp", "w")
            print(out_text, file = f)


if __name__ == "__main__":
    main()