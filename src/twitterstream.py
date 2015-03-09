import oauth2 as oauth
import urllib2 as urllib
import sys

'''
I created a separate credentials file to hide my
credentials since I've uploaded this code to my
GitHub page.
'''
credentialsFile = open('../res/twitter-keys.txt', 'r')

api_key = credentialsFile.readline().rstrip('\n')
api_secret = credentialsFile.readline().rstrip('\n')
access_token_key = credentialsFile.readline().rstrip('\n')
access_token_secret = credentialsFile.readline().rstrip('\n')

_debug = 0
oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
http_method = "GET"
http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)
    return response

'''
Slight modifications made to encorporate English-only tweets,
writing directly to a specified output file, and specifying
the number of tweets to capture before stopping.
'''
def fetchsamples(file_path, number_of_tweets):
    url = "https://stream.twitter.com/1/statuses/sample.json"
    parameters = {'language': 'en'}  # Added language parameter to specify English-only tweets
    response = twitterreq(url, "GET", parameters)
    output_file = open(file_path, 'w')
    counter = 0
    for line in response:
        output_file.write(line.strip() + '\n')
        counter += 1
        if counter >= number_of_tweets:
            break

def main(output_path, number_of_tweets):
    fetchsamples(output_path, number_of_tweets)

if __name__ == '__main__':
    try:
        main(sys.argv[1], int(sys.argv[2]))
    except:
        sys.exit(
            "Please enter the desired path for the output file " +
            "and the number of tweets to collect as arguments in that order.")