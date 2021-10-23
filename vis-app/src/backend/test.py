import requests
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
                writer.writerow((items["id"], items["text"], items["created_at"], \
                items["place_id"], items["country"], items["city"],items["movie_name"] , \
                items["movie_id"]))

def delfile(file_name):
    os.remove("res.json")
    os.remove("res.txt")

def sqlentry(movie_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Login@123",
        database="Master_Final"
    )
    mycursor = mydb.cursor()
    # creating a table in db
    sql_query = "CREATE TABLE Master_Final." + movie_name + " (id VARCHAR(50), movie_name VARCHAR(75), text VARCHAR(500), created_at VARCHAR(75), place_id VARCHAR(75), country VARCHAR(75), city VARCHAR(100), PRIMARY KEY(id));"
    mycursor.execute(sql_query)
    with open(movie_name + ".json", "r") as rf:
        json_data = json.loads(rf.read())
        insert_query = "INSERT INTO Master_Final." + movie_name + " (movie_name, text, id, created_at, place_id, country, city) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        insert_vals = []
        if sql_entries == 1:
            for items in json_data["data"]:
                for item in items.values():
                    insert_vals.append(item)
            print(insert_query)
            print(insert_vals)
            mycursor.execute(insert_query, tuple(insert_vals))
        else:
            for items in json_data["data"]:
                for item in items.values():
                    dum_vals = []
                    dum_vals.append(item)
                    insert_vals.append(tuple(dum_vals))
            mycursor.executemany(insert_query, insert_vals)
        mydb.commit()
    # delfile(movie_name)

def connect_to_endpoint(bearer_token, next_token=None):
    global is_movie_empty
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    query = "lang:en has:geo (" + movie_names_list + ") place_country:US -is:retweet -is:quote -is:nullcast"
    print(query)
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
    response = requests.request("GET", url, params=params, headers=headers)

    if response.status_code != 200:
        print(response.text)
        print("waiting for 15 mins")
        time.sleep(900)
        response = requests.request("GET", url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
    
    if response.json()["meta"]["result_count"] == 0:
        is_movie_empty = True
        return "empty"
    else:
        is_movie_empty = False

    return data_restructure(response.json())

def data_restructure(response):
    data_arr = []
    global next_token, total_results, need_comma, sql_entries
    res_data = response["data"]
    geo_location = response["includes"]["places"]
    for item in res_data:
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
    total_results += int(response["meta"]["result_count"])
    if "next_token" in response["meta"]:
        next_token = response["meta"]["next_token"]
        need_comma = True
    else:    
        next_token = None
        need_comma = False
        if total_results == 1:
            sql_entries = 1
        # print(total_results)
    return data_arr

with open("tweetsv1.json", "r+") as rf:
    data = json.loads(rf.read())
    comma_for_next_file = 0
    for items in data["data"]:
        movie_id = items["movie_id"]
        # key = items["movie_name"]
        # val = items["list_of_mv_names"]
        key = "Blood Curse: The Haunting of Alicia Stone"
        val = "BloodCurse:TheHauntingofAliciaStone OR BloodCurse:TheHauntingofAliciaStonemovie OR BloodCurse:HauntingofAliciaStone OR BloodCurse:HauntingofAliciaStonemovie OR BloodCurse OR BloodCursemovie OR TheHauntingofAliciaStone OR TheHauntingofAliciaStonemovie OR HauntingofAliciaStone OR HauntingofAliciaStonemovie"
        next_token = "token"
        # if key == "Daddy's Girl":
        #     break
        print(key)
        movie_names_list = val
        movie_name = key
        while next_token is not None:
            if next_token == "token":
                next_token = None
            # print("next_token: ", next_token)
            time.sleep(1)
            res = connect_to_endpoint(bearer_token, next_token)
            if res == "empty":
                break
            # print(res)
            with open("senti.txt", 'a') as af:
                for i in res:
                    af.write(i["text"] +",")
            # with open("senti.csv", "w") as wf:
            #     writer = csv.writer(wf)
            #     with open("senti.txt", "r+") as rf:
            #         senti_data = rf.read()
            #         senti = TextBlob(senti_data).sentiment
            #         writer.writerow((movie_id, senti.polarity, senti.subjectivity))
            #         wf.truncate(0)
            with open("res.txt", 'a') as tf:
                # json.dumps => converts json to string
                # json.loads => converts string to json
                temp_data = json.dumps(res)
                str_data = ""
                if comma_for_next_file == 1:
                    str_data += ","
                str_data += temp_data[1:-1]
                # if need_comma:
                #     str_data += ","
                # tf.write(str_data)
                str_data += ","
                tf.write(str_data[0:-1])
                comma_for_next_file = 1
        if not is_movie_empty:
            with open("senti.csv", "a") as wf:
                writer = csv.writer(wf)
                with open("senti.txt", "r+") as rf:
                    senti_data = rf.read()
                    senti = TextBlob(senti_data).sentiment
                    writer.writerow((movie_id, senti.polarity, senti.subjectivity))
                    # rf.truncate(0)
        break

with open("res.txt", "r") as rf:
    txt_data = '{"data":['
    txt_data += rf.read()
    txt_data += "]}"
    with open("res.json", "w") as wf:
        data = json.loads(txt_data)
        data["result_count"] = total_results
        wf.write(json.dumps(data))





        # if (next_token is None) and (res != "empty"):
        #     txt_data = '{"data":['
        #     with open("res.txt", "r") as tf:
        #         txt_data += tf.read()
        #     txt_data += "]}"
        #     with open("res.json", "w") as jf:
        #         data = json.loads(txt_data)
        #         # print(data)
        #         data["result_count"] = total_results
        #         jf.write(json.dumps(data))
        # # writefile()
        # break
        







        # if key == "Synapse":
        #     break
        # movie_names_list = val
        # movie_name = key
        # while next_token is not None:
        #     if next_token == "token":
        #         next_token = None
        #     # print(key)
        #     # print(val)
        #     # print("next_token: ", next_token)
        #     time.sleep(1)
        #     res = connect_to_endpoint(bearer_token, next_token)
        #     if res == "empty":
        #         # print("empty")
        #         # print("\n")
        #         break
        #     # print("\n")
        #     with open(movie_name + ".txt", 'a') as tf:
        #         # json.dumps => converts json to string
        #         # json.loads => converts string to json
        #         temp_data = json.dumps(res)
        #         str_data = temp_data[1:-1]
        #         if need_comma:
        #             str_data += ","
        #         tf.write(str_data)
        # if (next_token is None) and (res != "empty"):
        #     txt_data = '{"data":['
        #     with open(movie_name + ".txt", "r") as tf:
        #         txt_data += tf.read()
        #     txt_data += "]}"
        #     with open(movie_name + ".json", "w") as jf:
        #         data = json.loads(txt_data)
        #         data["result_count"] = total_results
        #         jf.write(json.dumps(data))
        #     sqlentry(movie_name)










    # movie_names_list = data["Cruella"]
    # movie_name = "Cruella"
    # while next_token is not None:
    #     if next_token == "token":
    #         next_token = None
    #     print("next_token: ", next_token)
    #     time.sleep(1)
    #     res = connect_to_endpoint(bearer_token, next_token)
    #     with open(movie_name + ".txt", 'a') as tf:
    #         # json.dumps => converts json to string
    #         # json.loads => converts string to json
    #         temp_data = json.dumps(res)
    #         str_data = temp_data[1:-1]
    #         if need_comma:
    #             str_data += ","
    #         tf.write(str_data)
    # if next_token is None:
    #     txt_data = '{"data":['
    #     with open(movie_name + ".txt", "r") as tf:
    #         txt_data += tf.read()
    #     txt_data += "]}"
    #     with open(movie_name + ".json", "a") as jf:
    #         data = json.loads(txt_data)
    #         data["result_count"] = total_results
    #         jf.write(json.dumps(data))


# while next_token is not None:
#     if next_token == "token":
#         next_token = None
#     print("next_token: ", next_token)
#     time.sleep(1)
#     res = connect_to_endpoint(bearer_token, next_token)
#     with open("resp1.txt", 'a') as tf:
#         # json.dumps => converts json to string
#         # json.loads => converts string to json
#         temp_data = json.dumps(res)
#         str_data = temp_data[1:-1]
#         if need_comma:
#             str_data += ","
#         tf.write(str_data)

# if next_token is None:
#     txt_data = '{"data":['
#     with open("resp1.txt", "r") as tf:
#         txt_data += tf.read()
#     txt_data += "]}"
    
#     with open("resp1.json", "a") as jf:
#         data = json.loads(txt_data)
#         data["result_count"] = total_results
#         jf.write(json.dumps(data))

