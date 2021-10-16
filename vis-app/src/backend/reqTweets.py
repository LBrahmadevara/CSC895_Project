import requests
import json
import time

start_time = '2021-01-01T00:00:00Z'
end_time = '2021-07-01T00:00:00Z'
max_results = 500
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
bearer_token = "AAAAAAAAAAAAAAAAAAAAAH0JTgEAAAAA5V9Rho9fw%2FhTnIIxJEBrFUSPDUs%3D6vRoSA2pU4tpFhPjnJjavfmUarKYNHohGN1PV4PYkXapOMlVkr"
next_token = "token"
total_results = 0
need_comma = False

with open("resp.json", "r+") as file:
    file.truncate(0)

with open("resp.txt", "r+") as tf:
    tf.truncate(0)

def connect_to_endpoint(bearer_token, next_token=None):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    query = "lang:en has:geo (intheheights OR intheheightsmovie) place_country:US -is:retweet -is:quote -is:nullcast"
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
    return data_restructure(response.json())

def data_restructure(response):
    data_arr = []
    global next_token
    global total_results
    global need_comma
    res_data = response["data"]
    geo_location = response["includes"]["places"]
    for item in res_data:
        temp_data = {}
        temp_data["text"] = item["text"]
        temp_data["id"] = item["id"]
        temp_data["created_at"] = item["created_at"]
        temp_data["place_id"] = item["geo"]["place_id"]
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
    return data_arr

while next_token is not None:
    if next_token == "token":
        next_token = None
    print("next_token: ", next_token)
    time.sleep(1)
    res = connect_to_endpoint(bearer_token, next_token)
    with open("resp.txt", 'a') as tf:
        # json.dumps => converts json to string
        # json.loads => converts string to json
        temp_data = json.dumps(res)
        str_data = temp_data[1:-1]
        if need_comma:
            str_data += ","
        tf.write(str_data)

if next_token is None:
    txt_data = '{"data":['
    with open("resp.txt", "r") as tf:
        txt_data += tf.read()
    txt_data += "]}"
    with open("resp.json", "a") as jf:
        data = json.loads(txt_data)
        data["result_count"] = total_results
        jf.write(json.dumps(data))
