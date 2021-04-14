import json, requests
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

# Constantes
  
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console

        CONSUMER_KEY = "HBE7m9FTfdR7oC5awdcuDTS66"
        CONSUMER_SECRET = "hHDJBblupuLHephjNzxi9CKVwCGHqAAVec8sgsl4zX4BbtV85H"
        ACCESS_TOKEN = "1369335372094840838-Kur6OjM5AIqBj9xniAnz4B98sEOgB7"
        ACCESS_TOKEN_SECRET = "8SAyCy20rThI0ZBtQDNgoB4Wvp8nkSD9svIYBPFWVBMj8"
        #URL = "https://imdb-api.com/en/API/InTheaters/k_j8vk26rm"
     
  
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET)
            # set access token and secret
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
  
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
  
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
  
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
  
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
  
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
  
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def obtenerListaPeliculas():

    URL = "https://imdb-api.com/en/API/InTheaters/k_j8vk26rm"

    lista_peliculas = []

    response = requests.get(URL)    
    data = json.loads(response.text)
    
    file = open("data.json", "r")
    content = file.read()
    json_decoded = json.loads(content)

    for entity in json_decoded["items"]:
        lista_peliculas.append(entity["title"])

    return lista_peliculas
  
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets

    lista_peliculas = []
    lista_peliculas_ejemplo = []

    lista_peliculas_ejemplo.append("Matrix")
    lista_peliculas_ejemplo.append("Titanic")

    lista_peliculas = obtenerListaPeliculas()

    #tweets = api.get_tweets(query = 'Donald Trump', count = 200)
    
    for i in range(len(lista_peliculas_ejemplo)):
        #print("TITULO"+lista_peliculas[i])

        #tweets = api.get_tweets(query = lista_peliculas[i], count = 200)

        print("TITULO   "+lista_peliculas_ejemplo[i])

        tweets = api.get_tweets(query = lista_peliculas_ejemplo[i], count = 200)
    
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} % \
            ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
    
        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:10]:
            print(tweet['text'])
    
        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in ntweets[:10]:
            print(tweet['text'])
  
if __name__ == "__main__":
    # calling main function
    main()