import sys
import json
import string

def create_sentiment_dictionary(sentiment_file):
    sentiment_dictionary = {}
    for line in sentiment_file:
        word, sentiment_value  = line.split("\t")
        sentiment_dictionary[word] = int(sentiment_value)
    return sentiment_dictionary

def print_individual_sentiments(tweet_file, sentiment_dictionary):
    for line in tweet_file:
        tweet = json.loads(line)
        try:
            print calculate_tweet_sentiment(tweet["text"], sentiment_dictionary)
        except:
            pass  # JSON line doesn't have a text value

def calculate_tweet_sentiment(tweet, sentiment_dictionary):
    tweet = format_tweet(tweet)
    sentiment_value = 0
    for word in tweet.split():
        try:
            sentiment_value += sentiment_dictionary[word]
        except:
            pass  # Word not in sentiment dictionary
    return sentiment_value

def format_tweet(tweet):
    tweet = tweet.encode('utf-8')  #Encode string for unicode
    tweet = tweet.lower()  #Convert to lower case for accurate dictionary matching
    tweet = tweet.translate(string.maketrans("",""), string.punctuation)  #Remove punctuation for dictionary matching
    return tweet

def main():
    try:
        sentiment_file = open(sys.argv[1])
        tweet_file = open(sys.argv[2])
    except:
        sys.exit(
            "Please enter the file path to the sentiment file and the " +
            "file path to the JSON file (output from twitterstream.py) as " +
            "arguments in that order.")

    sentiment_dictionary = create_sentiment_dictionary(sentiment_file)
    print_individual_sentiments(tweet_file, sentiment_dictionary)

if __name__ == '__main__':
    main()
