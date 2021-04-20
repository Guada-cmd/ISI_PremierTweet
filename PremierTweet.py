import json, requests
import re
import tweepy
import csv
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Twitter Class for sentiment analysis.
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

def showMainOptions():

    print("-----------------------------------------------------------------------------------------------")
    print('''\nWlcome to the Premier Tweet aplication!\n
    1.- See new films.
    2.- See a list of tweets.
    3.- Sentiment analysis.
    4.- Exit.\n''')
    print("-----------------------------------------------------------------------------------------------")

def showOptionOne():

     print('''\nChoose what to do:
    1.- Movies in threaters.
    2.- Successful movies all the time.
    3.- Top movies.
    4.- Coming soon movies.
    5.- Exit.''')


def showOptionTwo():

     print('''\nChoose what to do:
    1.- List of tweets of movies in threaters.
    2.- List of tweets of successful movies all the time.
    3.- List of tweets of top movies.
    4.- List of tweets of coming soon movies.
    5.- Exit.''')


def showOptionThree():

    print('''\nChoose what to do:
    1.- Sentiment analysis movies in threaters.
    2.- Sentiment analysis successful movies all the time.
    3.- Sentiment analysis top movies.
    4.- Sentiment analysis coming soon movies.
    5.- Exit.''')


def establishmentOfRange(min_range: int, max_range: int) -> int:

    while True:

        option_choice = input()

        if not option_choice.isnumeric() or int(option_choice) < min_range or int(option_choice) > max_range:
            print('The choice must be a number between ' +
                  str(min_range)+' and ' + str(max_range))
            continue
        else:
            break

    return option_choice

def obtenerListaPeliculas(url: str) -> list:

    lista_peliculas = []
 
    response = requests.get(url)   
    data = json.loads(response.text) 

    for entity in data["items"]:
        lista_peliculas.append(entity["title"])
    
    if len(lista_peliculas):
        lista_peliculas = lista_peliculas[:10]

    return lista_peliculas

def menu_opcion_uno(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas):

    exit_sub_menu = False

    while not exit_sub_menu:

        showOptionOne()
        choice = establishmentOfRange(1, 5)
        menuChoice = int(choice)

        if menuChoice == 1:

            for i in range(len(lista_peliculas_cines)):
                print(str(i+1)+" Movie Title ---- "+lista_peliculas_cines[i]+"\n")

        elif menuChoice == 2:

            for i in range(len(lista_peliculas_exitosas)):
                print(str(i+1)+" Movie Title ---- "+lista_peliculas_exitosas[i]+"\n")
            

        elif menuChoice == 3:

            for i in range(len(lista_peliculas_top)):
                print(str(i+1)+" Movie Title ---- "+lista_peliculas_top[i]+"\n")

        elif menuChoice == 4:

            for i in range(len(lista_peliculas_proximas)):
                print(str(i+1)+" Movie Title ---- "+lista_peliculas_proximas[i]+"\n")
               
        elif menuChoice == 5:
            exit_sub_menu = True

def menu_opcion_dos(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas):

    exit_sub_menu = False

    while not exit_sub_menu:

        showOptionTwo()
        choice = establishmentOfRange(1, 5)
        menuChoice = int(choice)

        api = TwitterClient()

        if menuChoice == 1:
            
            for i in range(len(lista_peliculas_cines)):

                tweets = api.get_tweets(query = lista_peliculas_cines[i], count = 200)
                print("Teewst "+lista_peliculas_cines[i])
                
                for i in tweets[:10]:
                    print(i['text'])

        elif menuChoice == 2:
            
            for i in range(len(lista_peliculas_exitosas)):

                tweets = api.get_tweets(query = lista_peliculas_exitosas[i], count = 200)
                print("Teewst "+lista_peliculas_exitosas[i])
                
                for i in tweets[:10]:
                    print(i['text'])
           
        elif menuChoice == 3:

            for i in range(len(lista_peliculas_top)):

                tweets = api.get_tweets(query = lista_peliculas_top[i], count = 200)
                print("Teewst "+lista_peliculas_top[i])
                
                for i in tweets[:10]:
                    print(i['text'])

        elif menuChoice == 4:

            for i in range(len(lista_peliculas_proximas)):

                tweets = api.get_tweets(query = lista_peliculas_proximas[i], count = 200)
                print("Teewst "+lista_peliculas_proximas[i])
                
                for i in tweets[:10]:
                    print(i['text'])


        elif menuChoice == 5:
            exit_sub_menu = True


def printCSV(name, resumen_peliculas):

    fieldnames = ['category', 'movie_title', 'positive', 'neutral', 'negative']

    lista_pelicula_individual = []
    cadena_pelicula = ""

    with open(name, 'w', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(resumen_peliculas)):

            cadena_pelicula = resumen_peliculas[i]
            lista_pelicula_individual = cadena_pelicula.split('\n')

            writer.writerow({'category': 'movies_theaters', 'movie_title': lista_pelicula_individual[0], 
            'positive': lista_pelicula_individual[1], 'neutral': lista_pelicula_individual[2], 'negative': lista_pelicula_individual[3]})


def printSentimentAnalysis(api, lista_peliculas) -> list:

    positivo = ""
    negativo = ""
    neutral = ""
    resumen_analisis_sentimientos = []

    for i in range(len(lista_peliculas)):

        print(str(i+1)+" Movie Title ---- "+lista_peliculas[i]+"\n")
        tweets = api.get_tweets(query = lista_peliculas[i], count = 200)
    
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

        # percentage of positive tweets
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
        positivo = str((100*len(ptweets)/len(tweets)))

        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

        # percentage of negative tweets
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
        negativo = str((100*len(ntweets)/len(tweets)))

        # percentage of neutral tweets
        print("Neutral tweets percentage: {} % \
            ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))+"\n")

        neutral = str(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))

        resumen_analisis_sentimientos.append(lista_peliculas[i]+"\n"+str(positivo)+"\n"+str(neutral)+"\n"+str(negativo))

        print("-------")
    
    return resumen_analisis_sentimientos

def menu_opcion_tres(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas):

    exit_sub_menu = False

    api = TwitterClient()

    # Lista con los datos que tendran los datos del analisis de sentimientos

    resumen_peliculas_cines = []
    resumen_peliculas_exitosas = []
    resumen_peliculas_top = []
    resumen_peliculas_proximas = []

    while not exit_sub_menu:

        showOptionThree()
        choice = establishmentOfRange(1, 5)
        menuChoice = int(choice)

        if menuChoice == 1:

            resumen_peliculas_cines = printSentimentAnalysis(api, lista_peliculas_cines)
            printCSV('theaters_movies.csv', resumen_peliculas_cines)

        elif menuChoice == 2:

            resumen_peliculas_exitosas = printSentimentAnalysis(api, lista_peliculas_exitosas)
            printCSV('success_movies.csv', resumen_peliculas_exitosas)

        elif menuChoice == 3:

            resumen_peliculas_top = printSentimentAnalysis(api, lista_peliculas_top)
            printCSV('top_movies.csv', resumen_peliculas_top)

        elif menuChoice == 4:

            resumen_peliculas_proximas = printSentimentAnalysis(api, lista_peliculas_proximas)
            printCSV('coming_soon_movies.csv', resumen_peliculas_proximas)
               
        elif menuChoice == 5:
            exit_sub_menu = True

def main(): 

    exit_sub_menu = False

    # Lista de peliculas

    lista_peliculas_cines = []
    lista_peliculas_exitosas = []
    lista_peliculas_top = []
    lista_peliculas_proximas = []

    # URL

    URL_MOVIES_THEATERS = "https://imdb-api.com/en/API/InTheaters/k_57tfjuqc"
    URL_SUCCESS_MOVIES_ALL_TIME = "https://imdb-api.com/en/API/BoxOfficeAllTime/k_57tfjuqc"
    URL_TOP_MOVIES = "https://imdb-api.com/en/API/Top250Movies/k_57tfjuqc"
    URL_COMING_SOON_MOVIES = "https://imdb-api.com/en/API/ComingSoon/k_57tfjuqc"

    lista_peliculas_cines = obtenerListaPeliculas(URL_MOVIES_THEATERS)
    lista_peliculas_exitosas = obtenerListaPeliculas(URL_SUCCESS_MOVIES_ALL_TIME)
    lista_peliculas_top = obtenerListaPeliculas(URL_TOP_MOVIES)
    lista_peliculas_proximas = obtenerListaPeliculas(URL_COMING_SOON_MOVIES)

    while not exit_sub_menu:

        showMainOptions()

        choice = establishmentOfRange(1, 4)
        menuChoice = int(choice)

        if menuChoice == 1:
          
            menu_opcion_uno(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas)
            
        elif menuChoice == 2:

            menu_opcion_dos(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas)

        elif menuChoice == 3:

           menu_opcion_tres(lista_peliculas_cines, lista_peliculas_exitosas, lista_peliculas_top, lista_peliculas_proximas)

        elif menuChoice == 4:

            exit_sub_menu = True
                

if __name__ == "__main__":
    
    main()
