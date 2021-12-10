from itertools import count, product
import mysql.connector
from flask import Flask, request
import json
import os


app = Flask(__name__)

genres = ["Action", "Animation", "Adventure", "Comedy", "Crime",
          "Documentary", "Drama", "Mystery", "Science Fiction", "Family"]

states = ['all', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'AC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
film_types = ["Combined Films", "Featured Film", "OTT Film"]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Login@123",
    database="Master_Final"
)

mycursor = mydb.cursor()

json_data = dict()

def getProductForMovieStateTypes():
    drop_down_list = list(product(states, film_types))
    return drop_down_list


def json_format(state_type, movie_type, key1, key2, values):

    if os.path.isfile("./json_files/{}.json".format(state_type)):
        f = open("./json_files/{}.json".format(state_type))
        json_data = json.load(f)
    else:
        json_data = dict()

    if state_type not in json_data.keys():
        json_data[state_type] = dict()
        json_data[state_type][movie_type] = dict()
        json_data[state_type][movie_type][key1] = dict()
        json_data[state_type][movie_type][key1][key2] = values
    elif movie_type not in json_data[state_type].keys():
        json_data[state_type][movie_type] = dict()
        json_data[state_type][movie_type][key1] = dict()
        json_data[state_type][movie_type][key1][key2] = values
    elif key1 not in json_data[state_type][movie_type].keys():
        json_data[state_type][movie_type][key1] = dict()
        json_data[state_type][movie_type][key1][key2] = values
    # elif key2 not in json_data[state_type][movie_type][key1].keys():
    else:
        json_data[state_type][movie_type][key1][key2] = values

    json_output = json.dumps(json_data, indent = 4)
    with open("./json_files/{}.json".format(state_type), "w") as outfile:
        outfile.write(json_output)


# this generates different combination of genres
def getProductForGenres():
    genreList = list(product(genres, repeat=2))
    return genreList


# retrieves the result for the queries
def MYSql(query):
    global mycursor
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if myresult[0][0] is None:
        return 0
    return myresult[0][0]


# 1st circle values => this gives the matrix for chord diagram
def chord_values(state_type, movie_type):
    genreList = getProductForGenres()
    data = []
    dummy_list = []
    for index, (i, j) in enumerate(genreList):
        if i == j:
            sql_query = ""
            if movie_type == "Combined Films":
                sql_query += "select count(*) from Master_Final.moviesv4 where genre = '{}'".format(
                    i)
                if state_type != "all":
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre = '{}' and allTweets.city LIKE '%{}%';".format(i, state_type)
            else:
                sql_query += "select count(*) from Master_Final.moviesv4 where genre = '{}' and movie_type = '{}';".format(
                    i, movie_type)
                if state_type == "all":
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre = '{}' and moviesv4.movie_type='{}';".format(i, movie_type)
                else:
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre = '{}' and allTweets.city LIKE '%{}%' and moviesv4.movie_type='{}';".format(i, state_type, movie_type)
            sql_result = MYSql(sql_query)
            dummy_list.append(sql_result)
        else:
            sql_query = ""
            if movie_type == "Combined Films":
                sql_query += "select count(*) from Master_Final.moviesv4 where genre LIKE '%{}%' and genre LIKE '%{}%'".format(i, j)
                if state_type != "all":
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre LIKE '%{}%' and moviesv4.genre LIKE '%{}%' and allTweets.city LIKE '%{}%';".format(i, j, state_type)
            else:
                sql_query += "select count(*) from Master_Final.moviesv4 where genre LIKE '%{}%' and genre LIKE '%{}%' and movie_type = '{}';".format(
                    i, j, movie_type)
                if state_type == "all":
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre LIKE '%{}%' and moviesv4.genre LIKE '%{}%' and moviesv4.movie_type='{}';".format(i, j, movie_type)
                else:
                    sql_query = ""
                    sql_query += "SELECT count(distinct(allTweets.movie_id)) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
                    moviesv4.genre LIKE '%{}%' and moviesv4.genre LIKE '%{}%' and allTweets.city LIKE '%{}%' and moviesv4.movie_type='{}';".format(i, j, state_type, movie_type)
            sql_result = MYSql(sql_query)
            dummy_list.append(sql_result)
        if (index+1) % len(genres) == 0:
            data.append(dummy_list)
            dummy_list = []
    print(data)
    return {"matrix": data}
# movie_type("CA", "Combined Films")
def movies_count_for_labels(state_type, movie_type):
    label_data = []
    label_movies_count_combined = []
    for genre in genres:
        sql_query = "SELECT count(distinct(allTweets.movie_id))FROM moviesv4 \
        JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and moviesv4.genre LIKE '%{}%' \
        and allTweets.city LIKE '%{}%'".format(genre, state_type)
        feature = MYSql(sql_query + " and moviesv4.movie_type='Featured Film'")
        ott = MYSql(sql_query + " and moviesv4.movie_type='OTT Film'")
        label_data.append([feature, ott])
        label_movies_count_combined.append(feature+ott)
    print(label_data)
    print(label_movies_count_combined)
    return {"movies_count_combined": label_movies_count_combined, "movies_count": label_data}
# movies_count_for_labels("CA", "Combined Films")
# 1st circle values => this gives the matrix for chord diagram


# chord ribbon values
def structured_sql_query_for_combined_genres(movie_type, state_type):
    sql_query = ""
    if movie_type == "Combined Films":
        sql_query += "SELECT count(*) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id"
        if state_type != "all":
            sql_query = ""
            sql_query += "SELECT count(*) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
            allTweets.city LIKE '%{}%'".format(state_type)
    else:
        sql_query += "SELECT count(*) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id \
        and movie_type = '{}'".format(movie_type)
        if state_type == "all":
            sql_query = ""
            sql_query += "SELECT count(*) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
            moviesv4.movie_type='{}'".format(movie_type)
        else:
            sql_query = ""
            sql_query += "SELECT count(*) FROM moviesv4 JOIN allTweets ON moviesv4.movie_id = allTweets.movie_id and \
            allTweets.city LIKE '%{}%' and moviesv4.movie_type='{}'".format(state_type, movie_type)
    # print(sql_query)
    return sql_query

def combined_genres_tweets(state_type, movie_type):
    genreList = getProductForGenres()
    pos = 0.25
    neg = -0.25
    tweet_count = []
    dummy_tweet_count = []
    avg_senti = []
    dummy_avg_senti = []
    senti = []
    dummy_senti = []
    ribbion_movies_count = []
    dummy_ribbion_movies_count = []
    for index, (i, j) in enumerate(genreList):
        sql_query = structured_sql_query_for_combined_genres(
            movie_type, state_type)
        if i == j:
            sql_query += " and genre = '{}'".format(i)
            sql_query_movies = sql_query[0:7] + \
                "count(distinct(moviesv4.movie_id))" + sql_query[15:]
            sql_query_for_avg_senti = sql_query[0:7] + \
                "avg(allTweets.polarity)" + sql_query[15:]
            sql_query_pos = sql_query + \
                " and allTweets.polarity >= {} and allTweets.polarity <= 1".format(
                    pos)
            sql_query_neu = sql_query + \
                " and allTweets.polarity < {} and allTweets.polarity > {}".format(
                    pos, neg)
            sql_query_neg = sql_query + \
                " and allTweets.polarity <= {} and allTweets.polarity >= -1".format(
                    neg)
            sql_result = MYSql(sql_query_for_avg_senti)
            dummy_tweet_count.append(MYSql(sql_query))
            dummy_avg_senti.append(round(sql_result, 2))
            dummy_senti.append([MYSql(sql_query_pos), MYSql(
                sql_query_neu), MYSql(sql_query_neg)])
            dummy_ribbion_movies_count.append(MYSql(sql_query_movies))

        else:
            sql_query += " and genre LIKE '%{}%' and genre LIKE '%{}%'".format(
                i, j)
            sql_query_movies = sql_query[0:7] + \
                "count(distinct(moviesv4.movie_id))" + sql_query[15:]
            sql_query_for_avg_senti = sql_query[0:7] + \
                "avg(allTweets.polarity)" + sql_query[15:]
            sql_query_pos = sql_query + \
                " and allTweets.polarity >= {} and allTweets.polarity <= 1".format(
                    pos)
            sql_query_neu = sql_query + \
                " and allTweets.polarity < {} and allTweets.polarity > {}".format(
                    pos, neg)
            sql_query_neg = sql_query + \
                " and allTweets.polarity <= {} and allTweets.polarity >= -1".format(
                    neg)
            sql_result = MYSql(sql_query_for_avg_senti)
            dummy_tweet_count.append(MYSql(sql_query))
            dummy_avg_senti.append(round(sql_result, 2))
            dummy_senti.append([MYSql(sql_query_pos), MYSql(
                sql_query_neu), MYSql(sql_query_neg)])
            dummy_ribbion_movies_count.append(MYSql(sql_query_movies))

        if (index+1) % len(genres) == 0:
            tweet_count.append(dummy_tweet_count)
            avg_senti.append(dummy_avg_senti)
            senti.append(dummy_senti)
            ribbion_movies_count.append(dummy_ribbion_movies_count)
            dummy_tweet_count = []
            dummy_avg_senti = []
            dummy_senti = []
            dummy_ribbion_movies_count = []
    print(tweet_count)
    print(avg_senti)
    print(senti)
    print(ribbion_movies_count)
    return {"tweet_count": tweet_count, "avg_senti": avg_senti, "overall_senti": senti, "ribbon_movies_count": ribbion_movies_count}
# combined_genres_tweets("all", "Featured Film")
# chord ribbon values


# 4th circle => tweet sentiment
def tweet_sentiment(state_type, movie_type):
    data = []
    tweet_count = []
    pos = 0.25
    neg = -0.25
    for genre in genres:
        sql_query = structured_sql_query_for_combined_genres(
            movie_type, state_type)
        sql_query += " and genre LIKE '%{}%'".format(genre)
        print(sql_query)
        sql_query_for_avg_senti = sql_query[0:7] + \
            "avg(allTweets.polarity)" + sql_query[15:]
        sql_query_pos = sql_query + \
            " and allTweets.polarity >= {} and allTweets.polarity <= 1".format(
                pos)
        sql_query_neu = sql_query + \
            " and allTweets.polarity < {} and allTweets.polarity > {}".format(
                pos, neg)
        sql_query_neg = sql_query + \
            " and allTweets.polarity <= {} and allTweets.polarity >= -1".format(
                neg)
        sql_result = MYSql(sql_query_for_avg_senti)
        tweet_count.append(MYSql(sql_query))
        data.append([MYSql(sql_query_pos), MYSql(sql_query_neu),
                    MYSql(sql_query_neg), round(sql_result, 2)])
    print(data)
    print(tweet_count)
    return {"tweets_senti_overall": data, "tweet_count":tweet_count}
# tweet_sentiment("all", "Featured Film")
# 4th circle => tweet sentiment


# saving the data for dropdown in json files
def save_data_in_json():
    for row in getProductForMovieStateTypes():
        print(row)
        movies_count_chord_values = movies_count_for_labels(row[0],row[1])
        ribbon_values = combined_genres_tweets(row[0], row[1])
        tweet_values = tweet_sentiment(row[0], row[1])
        json_format(row[0], row[1], "main_chord_values", "matrix", chord_values(row[0],row[1])["matrix"])
        json_format(row[0], row[1], "main_chord_values", "movies_count_combined", movies_count_chord_values["movies_count_combined"])
        json_format(row[0], row[1], "main_chord_values", "movies_count", movies_count_chord_values["movies_count"])
        json_format(row[0], row[1], "ribbon_values", "movies_count", ribbon_values["ribbon_movies_count"])
        json_format(row[0], row[1], "ribbon_values", "tweet_count", ribbon_values["tweet_count"])
        json_format(row[0], row[1], "ribbon_values", "avg_senti", ribbon_values["avg_senti"])
        json_format(row[0], row[1], "ribbon_values", "overall_senti", ribbon_values["overall_senti"])
        json_format(row[0], row[1], "tweet_senti_values", "tweet_count", tweet_values["tweet_count"])
        json_format(row[0], row[1], "tweet_senti_values", "tweets_senti_overall", tweet_values["tweets_senti_overall"])
# save_data_in_json()
# saving the data for dropdown in json files

# def dropdown_values(state_type, movie_type):
@app.route("/dropdown-chord-values", methods=["POST"])
def dropdown_values():
    state_type = request.get_json()["state_type"]
    movie_type = request.get_json()["movie_type"]
    if movie_type == "OTT Films":
        movie_type = movie_type[:-1]
    elif movie_type == "Feature Films":
        movie_type = "Featured Film"
    with open("./json_files/{}.json".format(state_type), "r") as rf:
        data = json.load(rf)
        values = data[state_type][movie_type]
        print("state_type: {}, movie_type: {}".format(state_type, movie_type))
        return values

# dropdown_values("CA", "Combined Films")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
