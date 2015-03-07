import sys

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def createSentimentDictionary():
	sentimentFile = open("../res/AFINN-111.txt")
	createSentimentDictionary = {} # initialize an empty dictionary
	for line in sentimentFile:
		word, sentimentValue  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		createSentimentDictionary[word] = int(sentimentValue)  # Convert the sentimentValue to an integer.

	return createSentimentDictionary


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()
