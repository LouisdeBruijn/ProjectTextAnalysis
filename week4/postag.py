import nltk
import sys

def main(argv):
    path = argv[1]
    f = open(path)
    rawText = f.read()
    f.close()

    sents = rawText.split('\n') # tokenize rawText to sentences
    sents.pop() # remove useless newline at end of every file
    
    tokens = [sent.split()[3] for sent in sents]
    pos_tokens = nltk.pos_tag(tokens)
    for i in range(len(sents)):
        sents[i] += " " + pos_tokens[i][1]
    out_text = "\n".join(sents)
    
    f = open(path + ".pos", "w")
    print(out_text, file = f)
    
if __name__ == "__main__":
    main(sys.argv)