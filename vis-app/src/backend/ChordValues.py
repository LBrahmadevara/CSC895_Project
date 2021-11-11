from itertools import product
import mysql.connector

genres = ["Action", "Animation", "Adventure", "Comedy", "Crime", "Documentary", "Drama", "Mystery", "Science Fiction", "Family"]

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Login@123",
  database="Master_Final"
)

mycursor = mydb.cursor()

def getProductForGenres():
    genreList = list(product(genres, repeat=2))
    return genreList

def MYSql(query):
    global mycursor
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult[0][0]

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
        if (index+1)%10 == 0:
            data.append(genre_data)
            genre_data = []
    print(data)
    # data_sum = 0
    # for i in data:
    #     print(sum(i))
    #     data_sum += sum(i)
    # print(data_sum)
    
    return data

sqlQueries()
