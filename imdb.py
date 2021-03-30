import json, requests
import tweepy
from tweepy import OAuthHandler

url = "https://imdb-api.com/en/API/InTheaters/k_j8vk26rm"
response = requests.get(url)
data = json.loads(response.text)
peliculas = []


for i in range(5):
	peliculas.append(data["items"][i]["title"])
	

consumer_key = "HBE7m9FTfdR7oC5awdcuDTS66"
consumer_secret = "hHDJBblupuLHephjNzxi9CKVwCGHqAAVec8sgsl4zX4BbtV85H"
access_token = "1369335372094840838-Kur6OjM5AIqBj9xniAnz4B98sEOgB7"
access_token_secret = "8SAyCy20rThI0ZBtQDNgoB4Wvp8nkSD9svIYBPFWVBMj8"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
   
for i in (peliculas):
	for tweet in tweepy.Cursor(api.search,q=i,count=100, lang="en", since="2017-04-03").items():
		print (tweet.created_at, tweet.text)

