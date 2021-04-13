import json, requests
import tweepy
from tweepy import OAuthHandler

# Constantes

CONSUMER_KEY = "HBE7m9FTfdR7oC5awdcuDTS66"
CONSUMER_SECRET = "hHDJBblupuLHephjNzxi9CKVwCGHqAAVec8sgsl4zX4BbtV85H"
ACCESS_TOKEN = "1369335372094840838-Kur6OjM5AIqBj9xniAnz4B98sEOgB7"
ACCESS_TOKEN_SECRET = "8SAyCy20rThI0ZBtQDNgoB4Wvp8nkSD9svIYBPFWVBMj8"
URL = "https://imdb-api.com/en/API/InTheaters/k_j8vk26rm"


def obtenerListaPeliculas():

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

    lista_peliculas = []

    lista_peliculas = obtenerListaPeliculas()

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
 
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    list_tweets = []

    for i in (lista_peliculas):
	    for tweet in tweepy.Cursor(api.search,q=i,count=100, lang="en", since="2017-04-03").items(20):
		    list_tweets.append(tweet.text)


    # texto = "".join(list_tweets)

    # for i in range(len(list_tweets)):
    #     new_list.append(texto.split("\n")[i])
    #     print(i)
    




    new_list = []
    for i in range(len(list_tweets)):
        new_list.append(list_tweets[i].split("\n")[0])
        #print("Tweet",i, ":\n", list_tweets[i].split("\n")[0])

    j=0
    for i in new_list:
        print("\nTweet " , j ,":\n", i, "\n")
        j=j+1

    #print("Tercer tweet", (list_tweets[3]))



main()
   
