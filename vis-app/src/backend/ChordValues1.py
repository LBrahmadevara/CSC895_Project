from itertools import product
import mysql.connector
from flask import Flask, request
from operator import itemgetter


app = Flask(__name__)

genres = ["Action", "Animation", "Adventure", "Comedy", "Crime",
          "Documentary", "Drama", "Mystery", "Science Fiction", "Family"]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Login@123",
    database="Master_Final"
)

mycursor = mydb.cursor()


def getProductForGenres():
    genreList = list(product(genres, repeat=2))
    # print(genreList)
    return genreList
# getProductForGenres()


def MYSql(query):
    global mycursor
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    # print(query)
    # print(myresult)
    if myresult[0][0] is None:
        return 0
    return myresult[0][0]



@app.route("/chord-ribbon-values-movie-type")
def movie_type():
    feature_data = []
    OTT_data = []
    genreList = getProductForGenres()
    feature_genre_data = []
    OTT_genre_data = []
    for index, (i, j) in enumerate(genreList):
        if i == j:
            if (i == "Science Fiction") and (j == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and movie_type = 'Featured Film' and (genre = '{}' or genre = 'Sci-Fi');".format(i)
                sql_query_OTT = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and movie_type = 'OTT Film' and (genre = '{}' or genre = 'Sci-Fi');".format(i)
            else:
                sql_query = "select count(*) from Master_Final.moviesv3 where genre = '{}' and movie_type = 'Featured Film' and polarity is not NULL;".format(i)
                sql_query_OTT = "select count(*) from Master_Final.moviesv3 where genre = '{}' and movie_type = 'OTT Film' and polarity is not NULL;".format(i)
            sql_result = MYSql(sql_query)
            feature_genre_data.append(sql_result)
            sql_result_OTT = MYSql(sql_query)
            OTT_genre_data.append(sql_result_OTT)
        else:
            if (i == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and movie_type = 'Featured Film' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(j, i)
                sql_query_OTT = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and movie_type = 'OTT Film' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(j, i)
            elif (j == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and movie_type = 'Featured Film' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(i, j)
                sql_query_OTT = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and movie_type = 'OTT Film' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(i, j)
            else:
                sql_query = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and genre LIKE '%{}%' and movie_type = 'Featured Film' and polarity is not NULL;".format(i, j)
                sql_query_OTT = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and genre LIKE '%{}%' and movie_type = 'OTT Film' and polarity is not NULL;".format(i, j)
            sql_result = MYSql(sql_query)
            feature_genre_data.append(sql_result)
            sql_result_OTT = MYSql(sql_query_OTT)
            OTT_genre_data.append(sql_result_OTT)
        if (index+1) % len(genres) == 0:
            feature_data.append(feature_genre_data)
            feature_genre_data = []
            OTT_data.append(OTT_genre_data)
            OTT_genre_data = []
    print("feature_data", feature_data)
    print("OTT_data", OTT_data)
    return {"feature_data": feature_data, "OTT_data": OTT_data}
# movie_type()


@app.route("/chord-ribbon-values")
def sqlQueries():
    data = []
    genreList = getProductForGenres()
    genre_data = []
    for index, (i, j) in enumerate(genreList):
        if i == j:
            if (i == "Science Fiction") and (j == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and (genre = '{}' or genre = 'Sci-Fi');".format(i)
            else:
                sql_query = "select count(*) from Master_Final.moviesv3 where genre = '{}' and polarity is not NULL;".format(i)
            sql_result = MYSql(sql_query)
            genre_data.append(sql_result)
        else:
            if (i == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(j, i)
            elif (j == "Science Fiction"):
                sql_query = "select count(*) from Master_Final.moviesv3 where polarity is not NULL and genre LIKE '%{}%' and (genre LIKE '%{}%' or genre LIKE '%Sci-Fi%');".format(i, j)
            else:
                sql_query = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and genre LIKE '%{}%' and polarity is not NULL;".format(i, j)
            sql_result = MYSql(sql_query)
            genre_data.append(sql_result)
        if (index+1) % len(genres) == 0:
            data.append(genre_data)
            genre_data = []
    # print(data)
    # print("data sent")
    film_typ = film_type()
    # print(combined_genres_tweets("Combined"))
    print(data)
    movie_film_type_chord_values = movie_type()
    return {"chord_values": data, "film_type": film_typ["data"],
            "combined_movies_count": film_typ["combined"],
            "feature_chord_values": movie_film_type_chord_values["feature_data"],
            "ott_chord_values": movie_film_type_chord_values["OTT_data"],
            "tweet_sentiment_combined": tweetSentimentValues("Combined")["data"],
            "tweet_sentiment_featured": tweetSentimentValues("Feature")["data"],
            "tweet_sentiment_OTT": tweetSentimentValues("OTT")["data"],
            "combined_genres_tweets": combined_genres_tweets("Combined"),
            "featured_genres_tweets": combined_genres_tweets("Feature"),
            "OTT_genres_tweets": combined_genres_tweets("OTT"),
            "combined_overall_sentiment": OverallSentiment("Combined")["data"],
            "featured_overall_sentiment": OverallSentiment("Feature")["data"],
            "ott_overall_sentiment": OverallSentiment("OTT")["data"],
            # "overall_sentiment": OverallSentiment()["data"],
            # "TweetCountPerGenre": TweetCountPerGenre()["data"],
            "feature_TweetCountPerGenre": TweetCountPerGenre("Feature")["data"],
            "ott_TweetCountPerGenre": TweetCountPerGenre("OTT")["data"],
            "combined_TweetCountPerGenre": TweetCountPerGenre("combined")["data"],
            }
# @app.route("/film-type")


def film_type():
    films = []
    combined_films = []
    for genre in genres:
        dummy_films = []
        sqlQuery1 = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity is not NULL and movie_type='Featured Film';".format(genre)
        sqlQuery2 = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity is not NULL and movie_type='OTT Film';".format(genre)
        val1= MYSql(sqlQuery1)
        dummy_films.append(val1)
        val2 = MYSql(sqlQuery2)
        dummy_films.append(val2)
        combined_films.append(val1+val2)
        films.append(dummy_films)
        # films.append(val1+val2)
    print(films)
    return {"data": films, "combined": combined_films}
# film_type()


@app.route('/chord-sentiment')
def sentimentValues():
    senti_chord_values = []
    for genre in genres:
        values = []
        sqlQuery1 = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity >= 0.25 and polarity <= 1;".format(genre)
        sqlQuery2 = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity < 0.25 and polarity > -0.5;".format(genre)
        sqlQuery3 = "SELECT count(*) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity <= -0 and polarity >= -1;".format(genre)
        values.append(MYSql(sqlQuery1))
        values.append(MYSql(sqlQuery2))
        values.append(MYSql(sqlQuery3))
        senti_chord_values.append(values)
    # print(senti_chord_values)
    return {"data": senti_chord_values}


# @app.route('/overall-senti')
def OverallSentiment(isFeature):
    senti_values = []
    for genre in genres:
        if isFeature == "Feature":
            sqlQuery = "SELECT avg(polarity) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity is not NULL and movie_type='Featured Film';".format(
            genre)
        elif isFeature == "OTT":
            sqlQuery = "SELECT avg(polarity) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity is not NULL and movie_type='OTT Film';".format(
            genre)
        else:
            sqlQuery = "SELECT avg(polarity) FROM Master_Final.moviesv3 where genre LIKE '%{}%' and polarity is not NULL;".format(
            genre)
        result = MYSql(sqlQuery)
        senti_values.append(round(result, 2))
    # print(senti_values)
    return {"data": senti_values}


# @app.route('/tweet-count')
def TweetCountPerGenre(isFeature):
    tweet_count = []
    for genre in genres:
        if isFeature == "Feature":
            sqlQuery = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id \
            and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and moviesv3.movie_type='Featured Film';".format(genre)
        elif isFeature == "OTT":
            sqlQuery = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id \
            and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and moviesv3.movie_type='OTT Film';".format(genre)
        else:
            sqlQuery = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id \
            and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%';".format(genre)
        tweet_count.append(MYSql(sqlQuery))
    # print(tweet_count)
    return {"data": tweet_count}


# @app.route('/tweet-count-senti')
def tweetSentimentValues(isFeature):
    filmType = ""
    if isFeature == "Feature":
        filmType += " and moviesv3.movie_type = 'Featured Film';"
        # print(filmType)
        # print("asdd")
        senti_chord_values = [[52665, 162715, 121990], [212489, 498828, 378428], [158410, 312588, 230618], [167767, 329274, 238032], [
            27404, 67656, 51286], [295163, 768293, 566943], [195672, 447760, 330952], [36793, 97160, 75442], [32688, 106334, 80310], [132039, 239484, 173504]]
    elif isFeature == "OTT":
        filmType += " and moviesv3.movie_type = 'OTT Film';"
        senti_chord_values = [[22479, 58328, 43321], [14120, 30133, 22620], [22479, 58328, 43321], [11193, 25887, 19091], [
            8608, 22619, 17925], [0, 0, 0], [35138, 90052, 69472], [10573, 24577, 19594], [0, 0, 0], [793, 1510, 1097]]
    elif isFeature == "Combined":
        filmType += ";"
        senti_chord_values = [[75144, 221043, 165311], [226609, 528961, 401048], [180889, 370916, 273939], [178960, 355161, 257123], [
            36012, 90275, 69211], [295163, 768293, 566943], [230810, 537812, 400424], [47366, 121737, 95036], [32688, 106334, 80310], [132832, 240994, 174601]]
    # senti_chord_values = []
    # for genre in genres:
    #     values = []
    #     sqlQuery1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and allTweets.polarity >= 0.25 and allTweets.polarity <= 1".format(genre)
    #     sqlQuery2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and allTweets.polarity <0.25 and allTweets.polarity >-0.5".format(genre)
    #     sqlQuery3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and allTweets.polarity <= -0 and allTweets.polarity >=- 1".format(genre)
    #     values.append(MYSql(sqlQuery1+filmType))
    #     values.append(MYSql(sqlQuery2+filmType))
    #     values.append(MYSql(sqlQuery3+filmType))
    #     senti_chord_values.append(values)
    # print(senti_chord_values)
    # print("Tweet sentiment sent to frontend")
    return {"data": senti_chord_values}


# tweetSentimentValues("OTT")


# tweetSentimentValues()


# @app.route('/tweets-for-combined-genres')
def combined_genres_tweets(isFeature):
    # print("rinning")
    # data = []
    # data_senti = []
    # genreList = getProductForGenres()
    # genre_data = []
    # dummy_data = []
    # sql_qwery = ""

    # if isFeature == "Combined":
    #     sql_qwery += ";"
        
    # elif isFeature == "Feature":
    #     sql_qwery += " and moviesv3.movie_type = 'Featured Film';"
    # elif isFeature == "OTT":
    #     sql_qwery += " and moviesv3.movie_type = 'OTT Film';"
    # for index, (i, j) in enumerate(genreList):
    #     # dummy_data = []
    #     if i == j:
    #         if (i == "Science Fiction") and (j == "Science Fiction"):
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.25 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0.25 and allTweets.polarity >= -1 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #         else:
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre = '{}'".format(i)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre = '{}'".format(i)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.25 and moviesv3.genre = '{}'".format(i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0.25 and allTweets.polarity >= -1 and moviesv3.genre = '{}'".format(i)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre = '{}'".format(i)
    #         dummy_data.append(MYSql(sql_query1+sql_qwery))
    #         dummy_data.append(MYSql(sql_query2+sql_qwery))
    #         dummy_data.append(MYSql(sql_query3+sql_qwery))
    #         result = MYSql(sql_query4+sql_qwery)
    #         dummy_data.append(round(result, 2))
    #         sql_result = MYSql(sql_query+sql_qwery)
    #         genre_data.append(sql_result)
    #     else:
    #         if (i == "Science Fiction"):
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.25 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0.25 and allTweets.polarity >= -1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #         elif (j == "Science Fiction"):
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.25 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0.25 and allTweets.polarity >= -1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #         else:
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.25 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0.25 and allTweets.polarity >=-1 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #         dummy_data.append(MYSql(sql_query1+sql_qwery))
    #         dummy_data.append(MYSql(sql_query2+sql_qwery))
    #         dummy_data.append(MYSql(sql_query3+sql_qwery))
    #         result = MYSql(sql_query4+sql_qwery)
    #         dummy_data.append(round(result, 2))
    #         sql_result = MYSql(sql_query+sql_qwery)
    #         genre_data.append(sql_result)
    #     if (index+1) % len(genres) == 0:
    #         data.append(genre_data)
    #         data_senti.append(dummy_data)
    #         genre_data = []
    #         dummy_data = []
    # print(data)
    # print(data_senti)
    data=[[7859, 91735, 150667, 27845, 64036, 45, 84848, 51188, 131432, 1098], [91735, 171273, 374162, 380626, 47526, 60135, 30258, 75766, 62511, 376769], [150667, 374162, 1568, 355148, 3430, 38, 113250, 2665, 109387, 334269], [27845, 380626, 355148, 30237, 12593, 3711, 90621, 6291, 6892, 373802], [64036, 47526, 3430, 12593, 46, 5284, 40205, 59177, 352, 76], [45, 60135, 38, 3711, 5284, 751871, 211, 300, 15, 1619], [84848, 30258, 113250, 90621, 40205, 211, 228378, 47325, 90045, 99], [51188, 75766, 2665, 6291, 59177, 300, 47325, 4703, 35304, 4], [131432, 62511, 109387, 6892, 352, 15, 90045, 35304, 17292, 9370], [1098, 376769, 334269, 373802, 76, 1619, 99, 4, 9370, 1138]]
    data_senti=[[1607, 5519, 733, 0.06, 21176, 62522, 8037, 0.07, 38870, 101297, 10500, 0.1, 7909, 18449, 1487, 0.13, 17833, 42177, 4026, 0.12, 10, 28, 7, 0.06, 20456, 58393, 5999, 0.1, 14267, 33493, 3428, 0.12, 30541, 90888, 10003, 0.08, 524, 541, 33, 0.25], [21176, 62522, 8037, 0.07, 40919, 119083, 11271, 0.1, 123712, 221823, 28627, 0.14, 131639, 221987, 27000, 0.16, 13398, 31033, 3095, 0.12, 12727, 44594, 2814, 0.06, 8513, 19353, 2392, 0.11, 19660, 49525, 6581, 0.1, 13764, 42886, 5861, 0.06, 129940, 220251, 26578, 0.16], [38870, 101297, 10500, 0.1, 123712, 221823, 28627, 0.14, 461, 1014, 93, 0.14, 123125, 206936, 25087, 0.16, 1000, 2203, 227, 0.14, 8, 25, 5, 0.08, 33007, 75801, 4442, 0.12, 784, 1781, 100, 0.15, 26725, 74340, 8322, 0.09, 117237, 192962, 24070, 0.16], [7909, 18449, 1487, 0.13, 131639, 221987, 27000, 0.16, 123125, 206936, 25087, 0.16, 9162, 19196, 1879, 0.14, 4261, 7550, 782, 0.16, 725, 2506, 480, 0.04, 22750, 61676, 6195, 0.1, 1821, 4124, 346, 0.14, 2561, 3922, 409, 0.18, 129216, 218016, 26570, 0.16], [17833, 42177, 4026, 0.12, 13398, 31033, 3095, 0.12, 1000, 2203, 227, 0.14, 4261, 7550, 782, 0.16, 21, 23, 2, 0.23, 1498, 3385, 401, 0.12, 10497, 27362, 2346, 0.12, 16527, 38723, 3927, 0.12, 111, 224, 17, 0.16, 20, 50, 6, 0.1], [10, 28, 7, 0.06, 12727, 44594, 2814, 0.06, 8, 25, 5, 0.08, 725, 2506, 480, 0.04, 1498, 3385, 401, 0.12, 203287, 501451, 47133, 0.12, 45, 140, 26, 0.04, 88, 196, 16, 0.14, 2, 12, 1, 0.05, 511, 1041, 67, 0.16], [20456, 58393, 5999, 0.1, 8513, 19353, 2392, 0.11, 33007, 75801, 4442, 0.12, 22750, 61676, 6195, 0.1, 10497, 27362, 2346, 0.12, 45, 140, 26, 0.04, 70420, 142978, 14980, 0.14, 13968, 30244, 3113, 0.13, 25110, 58502, 6433, 0.12, 31, 65, 3, 0.16], [14267, 33493, 3428, 0.12, 19660, 49525, 6581, 0.1, 784, 1781, 100, 0.15, 1821, 4124, 346, 0.14, 16527, 38723, 3927, 0.12, 88, 196, 16, 0.14, 13968, 30244, 3113, 0.13, 978, 3376, 349, 0.08, 10175, 22667, 2462, 0.12, 2, 2, 0, 0.27], [30541, 90888, 10003, 0.08, 13764, 42886, 5861, 0.06, 26725, 74340, 8322, 0.09, 2561, 3922, 409, 0.18, 111, 224, 17, 0.16, 2, 12, 1, 0.05, 25110, 58502, 6433, 0.12, 10175, 22667, 2462, 0.12, 4787, 11447, 1058, 0.12, 2835, 6080, 455, 0.14], [524, 541, 33, 0.25, 129940, 220251, 26578, 0.16, 117237, 192962, 24070, 0.16, 129216, 218016, 26570, 0.16, 20, 50, 6, 0.1, 511, 1041, 67, 0.16, 31, 65, 3, 0.16, 2, 2, 0, 0.27, 2835, 6080, 455, 0.14, 346, 735, 57, 0.15]]
    return {"chord_values": data, "senti": data_senti}


combined_genres_tweets("Combined")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
