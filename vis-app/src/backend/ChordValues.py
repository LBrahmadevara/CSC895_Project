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
    # print("feature_data", feature_data)
    # print("OTT_data", OTT_data)
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
    # print(film_typ)
    movie_film_type_chord_values = movie_type()
    featdata = TweetCountPerGenre("Feature")["data"]
    ottdata = TweetCountPerGenre("OTT")["data"]
    # print(featdata)
    # print(ottdata)
    print(tweetSentimentValues("Combined")["data"])
    # print(TweetCountPerGenre("Feature")["data"]+TweetCountPerGenre("OTT")["data"])
    res_list = [featdata[i] + ottdata[i] for i in range(len(featdata))]
    # print(res_list)
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
    data = []
    data_senti = []
    genreList = getProductForGenres()
    genre_data = []
    dummy_data = []
    sql_qwery = ""
    if isFeature == "Combined":
        sql_qwery += ";"
        data = [
            [7859, 91735, 150667, 27845, 64036, 45, 84848, 51188, 131432, 1098],
            [91735, 171273, 374162, 380626, 47526,
                60135, 30258, 75766, 62511, 376769],
            [150667, 374162, 1568, 355148, 3430, 38, 113250, 2665, 109387, 334269],
            [27845, 380626, 355148, 30237, 12593, 3711, 90621, 6291, 6892, 373802],
            [64036, 47526, 3430, 12593, 46, 5284, 40205, 59177, 352, 76],
            [45, 60135, 38, 3711, 5284, 751871, 211, 300, 15, 1619],
            [84848, 30258, 113250, 90621, 40205, 211, 228378, 47325, 90045, 99],
            [51188, 75766, 2665, 6291, 59177, 300, 47325, 4703, 35304, 4],
            [131432, 62511, 109387, 6892, 352, 15, 90045, 35304, 17292, 9370],
            [1098, 376769, 334269, 373802, 76, 1619, 99, 4, 9370, 1138]
        ]
        data_senti = [
            [
                [1607, 5938, 4719, 0.06],
                [21176, 68109, 51558, 0.07],
                [38870, 108537, 81363, 0.1],
                [7909, 19400, 13701, 0.13],
                [17833, 44546, 33265, 0.12],
                [10, 34, 26, 0.06],
                [20456, 62224, 44453, 0.1],
                [14267, 35434, 26919, 0.12],
                [30541, 97740, 74172, 0.08],
                [524, 560, 400, 0.25],
            ],
            [
                [21176, 68109, 51558, 0.07],
                [40919, 126569, 101027, 0.1],
                [123712, 238240, 172189, 0.14],
                [131639, 236354, 171393, 0.16],
                [13398, 32815, 25023, 0.12],
                [12727, 46363, 36484, 0.06],
                [8513, 20772, 14821, 0.11],
                [19660, 53028, 42320, 0.1],
                [13764, 47138, 35906, 0.06],
                [129940, 234451, 169684, 0.16],
            ],
            [
                [38870, 108537, 81363, 0.1],
                [123712, 238240, 172189, 0.14],
                [461, 1073, 810, 0.14],
                [123125, 220468, 157949, 0.16],
                [1000, 2355, 1760, 0.14],
                [8, 30, 21, 0.08],
                [33007, 78559, 60680, 0.12],
                [784, 1846, 1431, 0.15],
                [26725, 80185, 60646, 0.09],
                [117237, 205811, 147670, 0.16],
            ],
            [
                [7909, 19400, 13701, 0.13],
                [131639, 236354, 171393, 0.16],
                [123125, 220468, 157949, 0.16],
                [9162, 20332, 15318, 0.14],
                [4261, 7972, 6077, 0.16],
                [725, 2797, 2308, 0.04],
                [22750, 65537, 45144, 0.1],
                [1821, 4334, 3113, 0.14],
                [2561, 4150, 3095, 0.18],
                [129216, 232209, 167864, 0.16],
            ],
            [
                [17833, 44546, 33265, 0.12],
                [13398, 32815, 25023, 0.12],
                [1000, 2355, 1760, 0.14],
                [4261, 7972, 6077, 0.16],
                [21, 25, 16, 0.23],
                [1498, 3648, 2647, 0.12],
                [10497, 28764, 22593, 0.12],
                [16527, 40987, 31235, 0.12],
                [111, 234, 176, 0.16],
                [20, 54, 37, 0.1],
            ],
            [
                [10, 34, 26, 0.06],
                [12727, 46363, 36484, 0.06],
                [8, 30, 21, 0.08],
                [725, 2797, 2308, 0.04],
                [1498, 3648, 2647, 0.12],
                [203287, 530585, 394889, 0.12],
                [45, 154, 132, 0.04],
                [88, 207, 169, 0.14],
                [2, 12, 9, 0.05],
                [511, 1082, 875, 0.16],
            ],
            [
                [20456, 62224, 44453, 0.1],
                [8513, 20772, 14821, 0.11],
                [33007, 78559, 60680, 0.12],
                [22750, 65537, 45144, 0.1],
                [10497, 28764, 22593, 0.12],
                [45, 154, 132, 0.04],
                [70420, 152110, 111612, 0.14],
                [13968, 31891, 24957, 0.13],
                [25110, 61972, 48377, 0.12],
                [31, 67, 39, 0.16],
            ],
            [
                [14267, 35434, 26919, 0.12],
                [19660, 53028, 42320, 0.1],
                [784, 1846, 1431, 0.15],
                [1821, 4334, 3113, 0.14],
                [16527, 40987, 31235, 0.12],
                [88, 207, 169, 0.14],
                [13968, 31891, 24957, 0.13],
                [978, 3588, 2921, 0.08],
                [10175, 23926, 19006, 0.12],
                [2, 2, 1, 0.27],
            ],
            [
                [30541, 97740, 74172, 0.08],
                [13764, 47138, 35906, 0.06],
                [26725, 80185, 60646, 0.09],
                [2561, 4150, 3095, 0.18],
                [111, 234, 176, 0.16],
                [2, 12, 9, 0.05],
                [25110, 61972, 48377, 0.12],
                [10175, 23926, 19006, 0.12],
                [4787, 12147, 8638, 0.12],
                [2835, 6338, 4930, 0.14],
            ],
            [
                [524, 560, 400, 0.25],
                [129940, 234451, 169684, 0.16],
                [117237, 205811, 147670, 0.16],
                [129216, 232209, 167864, 0.16],
                [20, 54, 37, 0.1],
                [511, 1082, 875, 0.16],
                [31, 67, 39, 0.16],
                [2, 2, 1, 0.27],
                [2835, 6338, 4930, 0.14],
                [346, 774, 556, 0.15],
            ],
        ]
    elif isFeature == "Feature":
        sql_qwery += " and moviesv3.movie_type = 'Featured Film';"
        # print("asd")
        data = [[7859, 72148, 68110, 6423, 63740, 45, 55454, 51188, 74391, 980], [72148, 168348, 354575, 369661, 47398, 60135, 27029, 75638, 31461, 375917], [68110, 354575, 1568, 333726, 3134, 38, 83856, 2665, 52346, 334151], [6423, 369661, 333726, 27248, 12448, 3711, 71821, 6222, 6811, 371942], [63740, 47398, 3134, 12448, 19, 5284,
                                                                                                                                                                                                                                                                                                          20070, 57022, 0, 1], [45, 60135, 38, 3711, 5284, 751871, 211, 300, 15, 1619], [55454, 27029, 83856, 71821, 20070, 211, 219135, 11314, 14050, 99], [51188, 75638, 2665, 6222, 57022, 300, 11314, 4702, 1729, 4], [74391, 31461, 52346, 6811, 0, 15, 14050, 1729, 17292, 9369], [980, 375917, 334151, 371942, 1, 1619, 99, 4, 9369, 1046]]
        data_senti = [[1607, 5938, 4719, 0.06, 15970, 54253, 41647, 0.06, 16391, 50209, 38042, 0.08, 2425, 3873, 2814, 0.18, 17745, 44344, 33124, 0.12, 10, 34, 26, 0.06, 12754, 41254, 29308, 0.09, 14267, 35434, 26919, 0.12, 14812, 57671, 43951, 0.05, 485, 484, 345, 0.27], [15970, 54253, 41647, 0.06, 40094, 124534, 99632, 0.1, 118506, 224384, 162278, 0.15, 127862, 229517, 165828, 0.16, 13357, 32731, 24952, 0.12, 12727, 46363, 36484, 0.06, 7686, 18549, 13231, 0.12, 19619, 52944, 42249, 0.1, 4465, 26227, 20457, -0.02, 129642, 233903, 169286, 0.16], [16391, 50209, 38042, 0.08, 118506, 224384, 162278, 0.15, 461, 1073, 810, 0.14, 117641, 204941, 147062, 0.16, 912, 2153, 1619, 0.13, 8, 30, 21, 0.08, 25305, 57589, 45535, 0.13, 784, 1846, 1431, 0.15, 10996, 40116, 30425, 0.05, 117198, 205735, 147615, 0.16], [2425, 3873, 2814, 0.18, 127862, 229517, 165828, 0.16, 117641, 204941, 147062, 0.16, 8135, 18418, 13898, 0.13, 4212, 7879, 6013, 0.16, 725, 2797, 2308, 0.04, 17992, 51862, 35595, 0.1, 1792, 4295, 3086, 0.14, 2556, 4074, 3023, 0.18, 128589, 231014, 166971, 0.16], [17745, 44344, 33124, 0.12, 13357, 32731, 24952, 0.12, 912, 2153, 1619, 0.13, 4212, 7879, 6013, 0.16, 8, 11, 7, 0.22, 1498, 3648, 2647, 0.12, 5330, 14310,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  11161, 0.12, 15899, 39528, 30070, 0.12, 0, 0, 0, 0, 0, 1, 0, 0.19], [10, 34, 26, 0.06, 12727, 46363, 36484, 0.06, 8, 30, 21, 0.08, 725, 2797, 2308, 0.04, 1498, 3648, 2647, 0.12, 203287, 530585, 394889, 0.12, 45, 154, 132, 0.04, 88, 207, 169, 0.14, 2, 12, 9, 0.05, 511, 1082, 875, 0.16], [12754, 41254, 29308, 0.09, 7686, 18549, 13231, 0.12, 25305, 57589, 45535, 0.13, 17992, 51862, 35595, 0.1, 5330, 14310, 11161, 0.12, 45, 154, 132, 0.04, 68175, 145490, 106289, 0.14, 3493, 7587, 5598, 0.15, 3666, 9902, 7841, 0.1, 31, 67, 39, 0.16], [14267, 35434, 26919, 0.12, 19619, 52944, 42249, 0.1, 784, 1846, 1431, 0.15, 1792, 4295, 3086, 0.14, 15899, 39528, 30070, 0.12, 88, 207, 169, 0.14, 3493, 7587, 5598, 0.15, 978, 3587, 2920, 0.08, 459, 1220, 923, 0.11, 2, 2, 1, 0.27], [14812, 57671, 43951, 0.05, 4465, 26227, 20457, -0.02, 10996, 40116, 30425, 0.05, 2556, 4074, 3023, 0.18, 0, 0, 0, 0, 2, 12, 9, 0.05, 3666, 9902, 7841, 0.1, 459, 1220, 923, 0.11, 4787, 12147, 8638, 0.12, 2834, 6338, 4930, 0.14], [485, 484, 345, 0.27, 129642, 233903, 169286, 0.16, 117198, 205735, 147615, 0.16, 128589, 231014, 166971, 0.16, 0, 1, 0, 0.19, 511, 1082, 875, 0.16, 31, 67, 39, 0.16, 2, 2, 1, 0.27, 2834, 6338, 4930, 0.14, 327, 701, 509, 0.15]]
    elif isFeature == "OTT":
        sql_qwery += " and moviesv3.movie_type = 'OTT Film';"
        data = [[7859, 72148, 68110, 6423, 63740, 45, 55454, 51188, 74391, 980], [72148, 168348, 354575, 369661, 47398, 60135, 27029, 75638, 31461, 375917], [68110, 354575, 1568, 333726, 3134, 38, 83856, 2665, 52346, 334151], [6423, 369661, 333726, 27248, 12448, 3711, 71821, 6222, 6811, 371942], [63740, 47398, 3134, 12448, 19, 5284,
                                                                                                                                                                                                                                                                                                          20070, 57022, 0, 1], [45, 60135, 38, 3711, 5284, 751871, 211, 300, 15, 1619], [55454, 27029, 83856, 71821, 20070, 211, 219135, 11314, 14050, 99], [51188, 75638, 2665, 6222, 57022, 300, 11314, 4702, 1729, 4], [74391, 31461, 52346, 6811, 0, 15, 14050, 1729, 17292, 9369], [980, 375917, 334151, 371942, 1, 1619, 99, 4, 9369, 1046]]
        data_senti = [[0, 0, 0, 0, 5206, 13856, 9911, 0.11, 22479, 58328, 43321, 0.12, 5484, 15527, 10887, 0.11, 88, 202, 141, 0.14, 0, 0, 0, 0, 7702, 20970, 15145, 0.11, 0, 0, 0, 0, 15729, 40069, 30221, 0.13, 39, 76, 55, 0.13], [5206, 13856, 9911, 0.11, 825, 2035, 1395, 0.13, 5206, 13856, 9911, 0.11, 3777, 6837, 5565, 0.17, 41, 84, 71, 0.16, 0, 0, 0, 0, 827, 2223, 1590, 0.1, 41, 84, 71, 0.16, 9299, 20911, 15449, 0.14, 298, 548, 398, 0.18], [22479, 58328, 43321, 0.12, 5206, 13856, 9911, 0.11, 0, 0, 0, 0, 5484, 15527, 10887, 0.11, 88, 202, 141, 0.14, 0, 0, 0, 0, 7702, 20970, 15145, 0.11, 0, 0, 0, 0, 15729, 40069, 30221, 0.13, 39, 76, 55, 0.13], [5484, 15527, 10887, 0.11, 3777, 6837, 5565, 0.17, 5484, 15527, 10887, 0.11, 1027, 1914, 1420, 0.17, 49, 93, 64, 0.16, 0, 0, 0, 0, 4758, 13675, 9549, 0.11, 29, 39, 27, 0.21, 5, 76, 72, 0.03, 627, 1195, 893, 0.16], [88, 202, 141, 0.14, 41, 84, 71, 0.16, 88, 202, 141, 0.14, 49, 93, 64, 0.16, 13, 14, 9, 0.24, 0, 0, 0, 0, 5167, 14454,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   11432, 0.11, 628, 1459, 1165, 0.13, 111, 234, 176, 0.16, 20, 53, 37, 0.1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7702, 20970, 15145, 0.11, 827, 2223, 1590, 0.1, 7702, 20970, 15145, 0.11, 4758, 13675, 9549, 0.11, 5167, 14454, 11432, 0.11, 0, 0, 0, 0, 2245, 6620, 5323, 0.09, 10475, 24304, 19359, 0.13, 21444, 52070, 40536, 0.12, 0, 0, 0, 0], [0, 0, 0, 0, 41, 84, 71, 0.16, 0, 0, 0, 0, 29, 39, 27, 0.21, 628, 1459, 1165, 0.13, 0, 0, 0, 0, 10475, 24304, 19359, 0.13, 0, 1, 1, 0.0, 9716, 22706, 18083, 0.12, 0, 0, 0, 0], [15729, 40069, 30221, 0.13, 9299, 20911, 15449, 0.14, 15729, 40069, 30221, 0.13, 5, 76, 72, 0.03, 111, 234, 176, 0.16, 0, 0, 0, 0, 21444, 52070, 40536, 0.12, 9716, 22706, 18083, 0.12, 0, 0, 0, 0, 1, 0, 0, 0.5], [39, 76, 55, 0.13, 298, 548, 398, 0.18, 39, 76, 55, 0.13, 627, 1195, 893, 0.16, 20, 53, 37, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0.5, 19, 73, 47, 0.12]]
    # for index, (i, j) in enumerate(genreList):
    #     # dummy_data = []
    #     if i == j:
    #         if (i == "Science Fiction") and (j == "Science Fiction"):
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.5 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0 and allTweets.polarity >= -1 and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and (moviesv3.genre = '{}' or moviesv3.genre = 'Sci-Fi')".format(i)
    #         else:
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre = '{}'".format(i)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre = '{}'".format(i)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.5 and moviesv3.genre = '{}'".format(i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0 and allTweets.polarity >= -1 and moviesv3.genre = '{}'".format(i)
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
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.5 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0 and allTweets.polarity >= -1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(j, i)
    #         elif (j == "Science Fiction"):
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.5 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0 and allTweets.polarity >= -1 and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #             sql_query4 = "SELECT avg(allTweets.polarity) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity is not NULL and moviesv3.genre LIKE '%{}%' and (moviesv3.genre LIKE '%{}%' or moviesv3.genre LIKE '%Sci-Fi%')".format(i, j)
    #         else:
    #             sql_query = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and moviesv3.polarity is not NULL and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query1 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity >= 0.25 and allTweets.polarity <= 1 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query2 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity < 0.25 and allTweets.polarity > -0.5 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
    #             sql_query3 = "SELECT count(*) FROM moviesv3 INNER JOIN allTweets ON moviesv3.movie_id = allTweets.movie_id and allTweets.polarity <= -0 and allTweets.polarity >=-1 and moviesv3.genre LIKE '%{}%' and moviesv3.genre LIKE '%{}%'".format(i, j)
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
    return {"chord_values": data, "senti": data_senti}


combined_genres_tweets("OTT")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
