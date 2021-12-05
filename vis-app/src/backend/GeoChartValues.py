from itertools import product
import mysql.connector
from flask import Flask, request
import csv

app = Flask(__name__)

statenames = [{'AL': 'Alabama'}, {'AK': 'Alaska'}, {'AZ': 'Arizona'}, {'AR': 'Arkansas'}, {'CA': 'California'}, {'CO': 'Colorado'}, {'CT': 'Connecticut'}, {'DE': 'Delaware'}, {'DC': 'District of Columbia'}, {'FL': 'Florida'}, {'GA': 'Georgia'}, {'HI': 'Hawaii'}, {'ID': 'Idaho'}, {'IL': 'Illinois'}, {'IN': 'Indiana'}, {'IA': 'Iowa'}, {'KS': 'Kansas'}, {'KY': 'Kentucky'}, {'LA': 'Louisiana'}, {'ME': 'Maine'}, {'MD': 'Maryland'}, {'MA': 'Massachusetts'}, {'MI': 'Michigan'}, {'MN': 'Minnesota'}, {'MS': 'Mississippi'}, {
    'MO': 'Missouri'}, {'MT': 'Montana'}, {'NE': 'Nebraska'}, {'NV': 'Nevada'}, {'NH': 'New Hampshire'}, {'NJ': 'New Jersey'}, {'NM': 'New Mexico'}, {'NY': 'New York'}, {'NC': 'North Carolina'}, {'ND': 'North Dakota'}, {'OH': 'Ohio'}, {'OK': 'Oklahoma'}, {'OR': 'Oregon'}, {'PA': 'Pennsylvania'}, {'RI': 'Rhode Island'}, {'SC': 'South Carolina'}, {'SD': 'South Dakota'}, {'TN': 'Tennessee'}, {'TX': 'Texas'}, {'UT': 'Utah'}, {'VT': 'Vermont'}, {'VA': 'Virginia'}, {'WA': 'Washington'}, {'WV': 'West Virginia'}, {'WI': 'Wisconsin'}, {'WY': 'Wyoming'}]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Login@123",
    database="Master_Final"
)
mycursor = mydb.cursor()


def MYSql(query):
    global mycursor
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult[0][0]


# @app.route('/geo-chart-values')
def values():
    tweet_count = {}
    tweet_senti = {}
    avg_senti = {}
    movies_count = {}
    for state in statenames:
        for key, val in state.items():
            senti = []
            sqlQuery1 = "SELECT count(*) FROM Master_Final.allTweets where city LIKE '%{}';".format(key)
            sqlQuery2 = "SELECT count(*) FROM Master_Final.allTweets where city LIKE '%{}' and allTweets.polarity >= 0.25 and allTweets.polarity <= 1;".format(key)
            sqlQuery3 = "SELECT count(*) FROM Master_Final.allTweets where city LIKE '%{}' and allTweets.polarity < 0.25 and allTweets.polarity >=-0.5;".format(key)
            sqlQuery4 = "SELECT count(*) FROM Master_Final.allTweets where city LIKE '%{}' and allTweets.polarity <= -0 and allTweets.polarity >= -1;".format(key)
            sqlQuery5 = "SELECT avg(polarity) FROM Master_Final.allTweets where city LIKE '%{}';".format(
                key)
            sqlQuery6 = "SELECT count(distinct movie_id) FROM Master_Final.allTweets where city LIKE '%{}';".format(
                key)
            tweet_count[val] = int(MYSql(sqlQuery1))
            senti.append(round(MYSql(sqlQuery2), 2))
            senti.append(round(MYSql(sqlQuery3), 2))
            senti.append(round(MYSql(sqlQuery4), 2))
            tweet_senti[val] = senti
            avg_senti[val] = round(MYSql(sqlQuery5), 2)
            movies_count[val] = MYSql(sqlQuery6)
    print(tweet_count)
    print(tweet_senti)
    print(avg_senti)
    print(movies_count)
    return {"tweet_count": tweet_count, "tweet_senti": tweet_senti, "avg_senti": avg_senti, "movies_count": movies_count}


# values()

tweet_count = [{'Alabama': 28559}, {'Alaska': 9584}, {'Arizona': 62265}, {'Arkansas': 13642}, {'California': 448679}, {'Colorado': 50666}, {'Connecticut': 26399}, {'Delaware': 3625}, {'District of Columbia': 30347}, {'Florida': 204114}, {'Georgia': 79700}, {'Hawaii': 15051}, {'Idaho': 7901}, {'Illinois': 112639}, {'Indiana': 49852}, {'Iowa': 18149}, {'Kansas': 16645}, {'Kentucky': 24268}, {'Louisiana': 41443}, {'Maine': 6275}, {'Maryland': 58947}, {'Massachusetts': 68100}, {'Michigan': 58158}, {'Minnesota': 35739}, {'Mississippi': 10980}, {'Missouri': 40936}, {
    'Montana': 3572}, {'Nebraska': 13638}, {'Nevada': 44617}, {'New Hampshire': 7017}, {'New Jersey': 76211}, {'New Mexico': 12366}, {'New York': 252243}, {'North Carolina': 118004}, {'North Dakota': 4321}, {'Ohio': 89054}, {'Oklahoma': 39804}, {'Oregon': 39241}, {'Pennsylvania': 86715}, {'Rhode Island': 9979}, {'South Carolina': 27200}, {'South Dakota': 3593}, {'Tennessee': 55256}, {'Texas': 321228}, {'Utah': 22574}, {'Vermont': 2456}, {'Virginia': 63163}, {'Washington': 67277}, {'West Virginia': 7479}, {'Wisconsin': 25762}, {'Wyoming': 1898}]

tweet_senti = [[8270, 19704, 14454], [2262, 7179, 5819], [17533, 43504, 32612], [3812, 9560, 7164], [129768, 310644, 228437], [14142, 35658, 26561], [7824, 18105, 13221], [877, 2657, 1821], [8019, 21820, 15698], [57208, 143331, 109475], [21235, 56953, 43115], [4359, 10432, 7880], [2282, 5479, 4064], [32466, 78167, 57069], [14517, 34382, 25223], [5507, 12356, 9048], [5075, 11325, 8115], [7183, 16678, 12113], [10752, 29836, 22618], [1864, 4306, 3064], [16103, 41565, 31119], [20029, 46833, 33708], [16621, 40460, 29852], [10635, 24493, 17450], [3175, 7581, 5677], [
    11863, 28311, 20701], [1018, 2499, 1720], [4076, 9350, 6562], [13083, 30645, 22685], [2003, 4905, 3574], [20883, 53854, 39994], [3312, 8840, 6228], [68887, 178947, 126031], [30479, 85970, 68401], [1478, 2773, 1908], [26180, 61197, 44690], [11771, 27446, 20573], [10683, 27484, 20667], [24200, 60809, 44922], [2926, 6853, 5055], [7513, 19251, 14613], [996, 2528, 1839], [16298, 37957, 27687], [94997, 220404, 164576], [6599, 15530, 11174], [690, 1728, 1259], [18061, 43901, 32207], [19334, 46772, 33552], [2277, 5073, 3561], [7525, 17743, 12939], [562, 1295, 963]]

movies_count = [619, 372, 782, 508, 1301, 724, 622, 343, 645, 999, 790, 518, 438, 894, 720, 544, 544, 626, 648, 408, 761, 817, 764, 676,
                457, 708, 326, 508, 753, 427, 815, 502, 1134, 774, 378, 814, 622, 674, 824, 478, 609, 320, 724, 1085, 621, 311, 794, 789, 420, 633, 264]

# print(tweet_count.values())
x = []
for i in tweet_count:
    # print(i)
    for val in i.values():
        x.append(val)
print(max(x))
print(min(x))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)