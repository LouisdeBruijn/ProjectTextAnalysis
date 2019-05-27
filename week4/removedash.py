import glob
import csv
import sys


def main(argv):
    path_list = glob.glob('group11/*/*/*.tok.off.pos.' + argv[1])
    print(path_list)
    for path in path_list:
        print(path)
        with open(path) as f:
            #csv_reader = csv.reader(csv_file, delimiter=' ')
            #for line in csv_reader:
            #    print(line)
            rawText = f.read()

            sents = rawText.split('\n') # tokenize rawText to sentences
            sents.pop() # remove useless newline at end of every file
            for i  in range(len(sents)):
                if sents[i].count(' ') == 6 and sents[i][-2:] == ' -':
                    sents[i] = sents[i][:-2]
            out_text = "\n".join(sents)

            f = open(path + ".nodash", "w")
            print(out_text, file = f)


if __name__ == "__main__":
    main(sys.argv)