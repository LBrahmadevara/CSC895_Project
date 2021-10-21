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

mycursor.execute("SELECT * FROM Master_Final.movies1;")
myresult = mycursor.fetchall()
# for i in myresult:
#   print(i)
with open("movies.csv", 'w', encoding="UTF8") as f:
    writer = csv.writer(f)
    # for x in myresult:
    writer.writerow(("Movie ID", "Movie Name", "Genre", "Year", "Movie Type", "Sentiment", "Release Date"))
    for x in myresult:
        writer.writerow(x)


