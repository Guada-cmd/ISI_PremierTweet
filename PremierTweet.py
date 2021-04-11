import json, requests
import tweepy

def main():
    while True:
        auth = tweepy.AppAuthHandler("HBE7m9FTfdR7oC5awdcuDTS66","hHDJBblupuLHephjNzxi9CKVwCGHqAAVec8sgsl4zX4BbtV85H")
        api = tweepy.API(auth)
        url = "https://imdb-api.com/en/API/InTheaters/k_j8vk26rm"
        response = requests.get(url)
        python_dictionary_values = json.loads(response.text)
        estrenos = python_dictionary_values.get('items')
        print("-----------------------------------------------------------------------------------------------")
        print("\n Welcome to the Premier Tweet aplication!\n\n1.See new films:\n2.See a list of Tweets\n3.Sentiment analysis (SOON)\n4.Exit\n\n")
        print("-----------------------------------------------------------------------------------------------")
        try:
            option = int(input(" Your option : "))
            if option == 1:
                i=0
                while i < len(estrenos):
                    print("\n "+estrenos[i].get("title")+"\n")
                    i=i+1
            elif option == 2:
                i=0
                while i <= len(estrenos):
                    print("\n NEXT FILM:"+estrenos[i].get("title")+"\n")
                    for tweet in tweepy.Cursor(api.search, q=estrenos[i].get("title")).items(20):
                        print(tweet.text)
                        i=i+1
            elif option == 3:
                print("\n Sentiment analysis coming soon!")
            elif option == 4:
                print()
                break
            else:
                print("Incorrect option, try again.")
        except:
            print("YOU HAVE TO PRINT A NUMBER!")

main()

