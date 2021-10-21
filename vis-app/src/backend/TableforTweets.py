# from reqTweets import connect_to_endpoint
import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Login@123",
  database="Master_Final"
)

mycursor = mydb.cursor()


def allFilms():
  # this takes movie_id from OTT1.csv file and checks whether the id is present in featured film
  #  if the id is present it updates the db by changing movie_type to Both
  #  else it inserts the rows from OTT1.csv to db
  #  to do this, need both featured and OTT films csv in seperate files
  with open("OTT1.csv", 'r') as rf:
    csvreader = csv.reader(rf)
    header = next(csvreader)
    for row in csvreader:
      id = row[0]
      select_query = "select count(movie_id) from Master_Final.featured where movie_id = " + id
      mycursor.execute(select_query)
      count = mycursor.fetchall()
      if count[0][0] == 1:
        print(count)
        update_query = 'update Master_Final.featured set movie_type = "Both" where movie_id = ' + id
        mycursor.execute(update_query)
        mydb.commit()
      else:
        insert_query = "Insert into Master_Final.featured (movie_id, movie_name, genre, year, movie_type,\
        sentiment, release_date) values (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(insert_query, tuple(row))
        mydb.commit()


def featuredFilm():
  #  by using react and flask we have already inserted feature films data to db
  #  here we are creating new csv file to insert all the data from db
  mycursor.execute("SELECT * FROM Master_Final.featured1;")
  myresult = mycursor.fetchall()
  with open("featured1.csv", 'w', encoding="UTF8") as f:
      writer = csv.writer(f)
      writer.writerow(("movie_id", "movie_name", "genre", "year", "movie_type", "sentiment", "release_date"))
      for x in myresult:
          writer.writerow(x)



# rows = []
# year_rows= []
# with open("movies1.csv", 'r') as rf:
#   csvreader = csv.reader(rf)
#   header = next(csvreader)
#   for row in csvreader:
#     sql_query = "insert into Master_Final.allMovies (movie_id, movie_name, genre, year, movie_type, \
#     sentiment, release_date) values (%s, %s, %s, %s, %s, %s, %s)"
#     sql_val = tuple(row)
#     mycursor.execute(sql_query, sql_val)
#     mydb.commit()


# for row in rows:
#   if row[-1].split('-')[0] == "2021":
#     year_rows.append(row)

