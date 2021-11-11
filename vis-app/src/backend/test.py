import requests
from datetime import datetime
from textblob import TextBlob
import mysql.connector
import json
import time
import csv
import os

# all_movie_names = {}
start_time = '2021-01-01T00:00:00Z'
end_time = '2021-10-01T00:00:00Z'
max_results = 500
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
bearer_token = "AAAAAAAAAAAAAAAAAAAAAH0JTgEAAAAA5V9Rho9fw%2FhTnIIxJEBrFUSPDUs%3D6vRoSA2pU4tpFhPjnJjavfmUarKYNHohGN1PV4PYkXapOMlVkr"
next_token = "token"
total_results = 0
need_comma = False
# need_comma = True
movie_name = ""
movie_names_list = ""
sql_entries = 0
movie_id = ""
is_movie_empty = False

# def readfile():
#     global movie_name, movie_names_list
#     with open("tweets.json", "r+") as rf:
#         data = json.loads(rf.read())
#         # for key, val in data.items():
#         #     connect_to_endpoint(bearer_token, key, val, None)
#         movie_names_list = data["Cruella"]
#         movie_name = "Cruella"
#         connect_to_endpoint(bearer_token, None)


def writefile():
    with open("TweetsList.json", "a") as wf:
        # writer = csv.writer(wf)
        filedata = {}
        with open("res.json", "r") as rf:
            data = json.loads(rf.read())
            for items in data["data"]:
                dum_data
                writer.writerow((items["id"], items["text"], items["created_at"],
                                 items["place_id"], items["country"], items["city"], items["movie_name"],
                                 items["movie_id"]))


def print_helper(msg):
    print("{}, Current Time: {}".format(msg, datetime.now().strftime("%H:%M:%S")))

def connect_to_endpoint(bearer_token, next_token=None):
    global is_movie_empty, movie_names_list
    result = None
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    movie_names_list = movie_names_list.replace(":", "")
    query = "lang:en has:geo (" + movie_names_list + \
        ") place_country:US -is:retweet -is:quote -is:nullcast"
    # print(query)
    params = {
        'tweet.fields': 'created_at,geo',
        'place.fields': 'country',
        'max_results': max_results,
        'start_time': start_time,
        'end_time': end_time,
        'query': query,
        'expansions': 'geo.place_id',
    }
    url = 'https://api.twitter.com/2/tweets/search/all'
    if (next_token is not None):
        params['next_token'] = next_token
    try:
        print_helper("Sending request")
        response = requests.request("GET", url, params=params, headers=headers, timeout=30)
        print_helper("Received response")
        if response.status_code == 400:
            print("\n")
            print("Error: {},{}".format(response.text, response.status_code))
        elif response.status_code != 200:
            print("\n")
            print(response.text, response.status_code)
            print_helper("waiting for 15 mins")
            time.sleep(960)
            print_helper("Sending request2")
            response = requests.request("GET", url, params=params, headers=headers, timeout=30)
            print_helper("Received response2")
            if response.status_code != 200:
                print_helper("Second Exception \n")
                raise Exception(response.status_code, response.text)
        if response.json()["meta"]["result_count"] == 0:
            is_movie_empty = True
            result = None
        else:
            is_movie_empty = False
            result = data_restructure(response.json())
    except Exception as err:
        print("\n")
        print("Error: connect_to endpoint: {}".format(repr(err)))
        print("\n")
    return result


def data_restructure(response):
    data_dic = {}
    data_arr = []
    global next_token, total_results, need_comma, sql_entries
    res_data = response["data"]
    geo_location = response["includes"]["places"]
    for item in res_data:
        try:
            temp_data = {}
            temp_data["movie_id"] = movie_id
            temp_data["movie_name"] = movie_name
            temp_data["text"] = item["text"]
            temp_data["id"] = item["id"]
            temp_data["created_at"] = item["created_at"]
            temp_data["place_id"] = item["geo"]["place_id"]
            sentiment_text = TextBlob(item["text"]).sentiment
            temp_data["polarity"] = sentiment_text.polarity
            temp_data["subjectivity"] = sentiment_text.subjectivity
            for geo_id in geo_location:
                if item["geo"]["place_id"] in geo_id.values():
                    temp_data["country"] = geo_id["country"]
                    temp_data["city"] = geo_id["full_name"]
            data_arr.append(temp_data)
        except Exception as err:
            print("\n")
            print_helper("Error: data_restructure: {}".format(repr(err)))
            print("\n")
    total_results += int(response["meta"]["result_count"])
    if "next_token" in response["meta"]:
        next_token = response["meta"]["next_token"]
        need_comma = True
    else:
        next_token = None
        need_comma = False
        if total_results == 1:
            sql_entries = 1
    data_dic["data"] = data_arr
    return data_dic

def files(file_name, token, data):
    if not os.path.isdir("files/{}".format(file_name)):
        os.mkdir("files/{}".format(file_name))
    with open("files/{}/{}.json".format(file_name, token), "w") as wf:
        wf.write(json.dumps(data))

with open("tweetsv1.json", "r+") as rf:
    data = json.loads(rf.read())
    comma_for_next_file = 0
    for items in data["data"]:
        movie_id = items["movie_id"]
        key = items["movie_name"]
        val = items["list_of_mv_names"]
        next_token = "token"
        print("\n")
        print_helper(key)
        movie_names_list = val
        movie_name = key
        while next_token is not None:
            if next_token == "token":
                next_token = None
            time.sleep(1)
            res = connect_to_endpoint(bearer_token, next_token)
            if res is None:
                break
            if next_token is None:
                files(movie_id, 1, res)
            else:
                files(movie_id, next_token, res)
