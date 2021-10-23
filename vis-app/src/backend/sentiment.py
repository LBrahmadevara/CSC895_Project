from textblob import TextBlob

testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
print(testimonial.sentiment)
# Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
# testimonial.sentiment.polarity