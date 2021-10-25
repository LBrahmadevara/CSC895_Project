from textblob import TextBlob
import csv

testimonial = TextBlob("You are a good girl, You are a bad girl")
print(testimonial.sentiment)
# Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
# testimonial.sentiment.polarity

# with open("senti.csv", "r") as rf:
#     data = csv.reader(rf)
#     update_query = "UPDATE allMoviesv1 SET polarity = %s, subjectivity = %s WHERE movie_id = %s"
#     for row in data:
#         query_val = [row[1], row[2], row[0]]
#         mycursor.execute(update_query, tuple(query_val))
#         mydb.commit()
