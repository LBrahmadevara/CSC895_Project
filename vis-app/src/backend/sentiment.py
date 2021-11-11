from textblob import TextBlob
import csv, os, json, time
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Login@123",
  database="Master_Final"
)

mycursor = mydb.cursor()

def sentiment_analysis(msg):
    sentiment = TextBlob(msg).sentiment
    # print(sentiment)
    return sentiment

def specific_movie_sentiment():
    for movie_id in os.listdir("senti"):
        # [1, 2, 3, 4]
    # for movie_id in range(1, 10):
        if not os.path.isdir("senti/{}".format(movie_id)):
            continue
        with open("senti/{}/movieSentiment.txt".format(movie_id), "r") as rf:
            print("movie_id: {}".format(movie_id))
            txt_data = rf.read()
            sentiment = sentiment_analysis(txt_data)
            with open("senti/overallmovieSenti.csv", "a") as af:
                writer = csv.writer(af)
                writer.writerow((movie_id, sentiment[0], sentiment[1]))


def update_movie_sentiment_sql():
    with open("senti/overallmovieSenti.csv", "r") as rf:
        csvreader = csv.reader(rf)
        for row in csvreader:
            time.sleep(1)
            print(row)
            # print(type(row[1]))
            update_query = "UPDATE Master_Final.moviesv2 SET polarity = {}, subjectivity = {} \
            WHERE movie_id = {}".format(row[1], row[2], row[0])
            mycursor.execute(update_query)
            mydb.commit()


def dict_to_arr(json_dict):
    tweet = []
    tweet.append(int(json_dict["movie_id"]))
    tweet.append(json_dict["movie_name"])
    x = ""
    for i in json_dict["text"].splitlines():
        x += i
    # tweet.append(json_dict["text"])
    tweet.append(x)
    tweet.append(json_dict["id"])
    tweet.append(json_dict["created_at"])
    tweet.append(json_dict["place_id"])
    tweet.append(json_dict["polarity"])
    tweet.append(json_dict["subjectivity"])
    tweet.append(json_dict["country"])
    tweet.append(json_dict["city"])
    return tuple(tweet)

def insert_tweets_sql():
    insert_query = "Insert into Master_Final.allTweets (movie_id, movie_name, tweet, \
    tweet_api_id, created_at, place_id, polarity, subjectivity, country, city) values \
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for movie_id in range(1, 5113):
        if not os.path.isdir("files/{}".format(movie_id)):
            continue
        print("movie_id :{}".format(movie_id))
        print("\n")
        for token_num in os.listdir("files/{}".format(movie_id)):
            # [1.json, asffds.json]
            time.sleep(0.25)
            all_tweets = []
            with open("files/{}/{}".format(movie_id, token_num), "r") as rf:
                json_data = json.loads(rf.read())
                for tweet in json_data["data"]:
                    tweet_tuple = dict_to_arr(tweet)
                    all_tweets.append(tweet_tuple)
            mycursor.executemany(insert_query, all_tweets)
            mydb.commit()

def files_to_do_sentiment():
    for movie_id in os.listdir("files"):
        # [1, 2, 3, 4]
        print("movie_id :{}".format(movie_id))
        if not os.path.isdir("files/{}".format(movie_id)):
            continue
        for token_num in os.listdir("files/{}".format(movie_id)):
            # [1.json, asdvsdfv.json]
            print("files/{}/{}".format(movie_id, token_num))
            with open("files/{}/{}".format(movie_id, token_num), "r") as rf:
                json_data = json.loads(rf.read())
                # print("json data: {}".format(json_data))
                for tweets in json_data["data"]:
                    tweet = tweets["text"]
                    #  creating a directory for a specific movie
                    if not os.path.isdir("senti/{}".format(movie_id)):
                        os.mkdir("senti/{}".format(movie_id))
                    # To insert all the tweets for a specific movie in txt
                    with open("senti/{}/movieSentiment.txt".format(movie_id), "a") as af:
                        af.write(tweet)
       
    
# files_to_do_sentiment()
# specific_movie_sentiment()
# update_movie_sentiment_sql()
# sentiment_analysis("Happy #Easter, #SolInvictus, #Ishtar, #Eostre, or #whatever. Have a good one. #HappyEaster2021 https://t.co/UMWViRL8z3")
insert_tweets_sql()
