import json, requests
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

from API_twitter import TwitterClient

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