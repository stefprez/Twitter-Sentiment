from __future__ import print_function
from time import sleep
from tweet_sentiment import calculate_tweet_sentiment, create_sentiment_dictionary
import twitterstream
import sys
import json
import datetime

def print_average_sentiment(tweet_file, sentiment_dictionary):
	date = datetime.datetime.now().date()
	time = datetime.datetime.now().time()
	average_sentiment = calculate_average_sentiment(tweet_file, sentiment_dictionary)
	print(date, time, average_sentiment, sep='\t')

def calculate_average_sentiment(tweet_file, sentiment_dictionary):
	total_sentiment = 0
	tweet_counter = 0
	for line in tweet_file:
		try:
			tweet = json.loads(line)
			total_sentiment += calculate_tweet_sentiment(tweet["text"], sentiment_dictionary)
			tweet_counter += 1
		except:
			pass  # Tweet file empty or tweet doesn't have a text value
	try:
		average_sentiment = float(total_sentiment) / tweet_counter
	except:
		if (tweet_counter == 0):
			average_sentiment = "Error: No Tweets Detected"
		else:
			average_sentiment = "Error: Unknown"
	return average_sentiment

def main():
	try:
		sentiment_file = open(sys.argv[1])
		output_file_path = sys.argv[2]
		number_of_tweets = int(sys.argv[3])
	except:
		sys.exit(
			"Please enter the path to the sentiment file, " + 
			"desired path for the Twitter Stream output, " + 
			"and the number of tweets to collect for each sample " + 
			"as arguments in that order.")


	headers = "Date\tTime\tAverage Sentiment"

	# Create sentiment dictionary
	sentiment_dictionary = create_sentiment_dictionary(sentiment_file)

	print("This script runs indefinitely. Press Ctrl+C to quit.")
	print(headers)

	while True:
		# Run twitter stream to generate json file
		twitterstream.main(output_file_path, number_of_tweets)

		# Open json tweet file and calculate average sentiment
		tweet_file = open(output_file_path)
		print_average_sentiment(tweet_file, sentiment_dictionary)

		# Wait five minutes
		sleep(300)

if __name__ == '__main__':
    main()
