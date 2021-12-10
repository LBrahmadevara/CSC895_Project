import time
from flask import Flask, request
import mysql.connector
import time
import csv

app = Flask(__name__)

data = []

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Login@123",
  database="Master_Final"
)
mycursor = mydb.cursor()

def isMovieTableCreated(table_name):
    istableCreated = False
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0] == table_name:
            istableCreated = True
    return istableCreated
        

def createMovieTable(table_name):
    sqlQuery = "CREATE TABLE " + table_name + " (movie_id VARCHAR(25), movie_name VARCHAR(255), genre VARCHAR(255), year VARCHAR(25), movie_type VARCHAR(25), sentiment VARCHAR(25), release_date VARCHAR(25), PRIMARY KEY (movie_id))"
    mycursor.execute(sqlQuery)

@app.route('/movieTable', methods=['POST'])
def insertMovies():
    table_name = "OTT"
    res = request.get_json()
    if not isMovieTableCreated(table_name):
        createMovieTable(table_name)
    for item in res["data"]:
        sqlquery = "Insert into Master_Final." + table_name + " ("
        sqlKey = ''
        sqlList = []
        for key, value in item.items():
            sqlKey += key + ", "
            sqlList.append(str(value))
        sqlquery += sqlKey[0:-2] + ") VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sqlquery, tuple(sqlList))
        mydb.commit()
    return "Flask running"


@app.route('/OTTmovies', methods=['POST'])
def OTTMovies():
    # using this logic, becoz whileinserting OTT films data, mysql is throwing an error
    res = request.get_json()
    global data
    for x in res["data"]:
        dum_data = []
        dum_data.append(x["movie_id"])
        dum_data.append(x["movie_name"])
        dum_data.append(x["genre"])
        dum_data.append(x["year"])
        dum_data.append(x["movie_type"])
        dum_data.append("")
        dum_data.append(x["release_date"])
        data.append(dum_data)
    if res["last_page"]:
        print(res["last_page"])
        with open("OTT1.csv", 'w', encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(("movie_id", "movie_name", "genre", "year", "movie_type", "sentiment", "release_date"))
            writer.writerows(data)
    return "OTT"

def insertsql():
    with open("allfilms.csv", "r") as rf:
        csvreader = csv.reader(rf)
        header = next(csvreader)
        for row in csvreader:
            insert_query = "Insert into Master_Final.allMoviesv1 (api_id, movie_name, \
            genre, year, movie_type,sentiment, release_date) values (%s, %s, %s, %s, %s, %s, %s)"
            mycursor.execute(insert_query, tuple(row))
            mydb.commit()

def createcsvfile():
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="Login@123",
    #     database="Master_Final"
    # )
    # mycursor = mydb.cursor()
    select_query = "SELECT * FROM Master_Final.allMoviesv1;"
    mycursor.execute(select_query)
    myresult = mycursor.fetchall()
    # print(myresult)
    with open("allMoviesv1.csv", "w", encoding="UTF8") as wf:
        writer = csv.writer(wf)
        writer.writerow(("movie_id", "api_id", "movie_name", "genre", "year", 
        "movie_type", "sentiment", "release_date"))
        for i in myresult:
            writer.writerow(i)

createcsvfile()


    # try this logic first, if its throwing an error, then use the above logic
    # table_name = "featured"
    # res = request.get_json()
    # for item in res["data"]:
    #     select_query = "select count(movie_id) from Master_Final." + table_name + " where movie_id = " + str(item["movie_id"])
    #     mycursor.execute(select_query)
    #     count = mycursor.fetchall()
    #     time.sleep(1)
    #     if count[0][0] == 1:
    #         update_query = "update Master_Final." + table_name + ' set movie_type = "Both" where movie_id = ' + str(item["movie_id"])
    #         mycursor.execute(update_query)
    #         mydb.commit()
    #     else:
    #         insert_query = "Insert into Master_Final." + table_name + " ("
    #         sql_key = ''
    #         sql_list = []
    #         for key, value in item.items():
    #             sql_key += key + ", "
    #             sql_list.append(str(value))
    #         insert_query += sql_key[0:-2] + ") VALUES (%s, %s, %s, %s, %s, %s)"
    #         mycursor.execute(insert_query, tuple(sql_list))
    #         mydb.commit()
    #     time.sleep(1)
    # return "OTT"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)