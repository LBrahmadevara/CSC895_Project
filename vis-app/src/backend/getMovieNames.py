# import requests
import json
import time
import csv

# all_movie_names = {}
all_movie_names_dict = {}
all_movie_names = []


def allFilms():
    # with open("allFilms.csv", 'r') as rf:
    with open("allMoviesv1.csv", 'r') as rf:
        csvreader = csv.reader(rf)
        header = next(csvreader)
        for row in csvreader:
            movie_id = row[0]
            x = {}
            # movie_names = []
            movie_names = []
            key = ""
            for i in row[2].split(" "):
                key += i
            names = row[2].split(" ")
            name1 = ""
            name2 = ""
            name3 = ""
            name4 = ""
            name5 = ""
            name6 = ""
            name7 = ""
            if (row[2] == "6:45") or (row[2] == "8:37 Rebirth"):
                continue
            if row[2] == "BLACKPINK :THE SHOW - Behind the Scenes":
                x["movie_id"] = movie_id
                x[row[2]] = "BLACKPINK OR BLACKPINKmovie"
                # x[row[2]] = ["BLACKPINK", "BLACKPINKmovie"]
                all_movie_names.append(x)
                x = {}
                # all_movie_names[row[2]] = ["BLACKPINK", "BLACKPINKmovie"]
                continue
            if ":" in row[2]:
                names1 = row[2].split(": ")
                names10 = names1[0].split(" ")
                for i in names10:
                    name4 += i
                    if i.lower() != "the":
                        name6 += i
                if len(names[1]) != 1:
                    names11 = names1[1].split(" ")
                    for i in names11:
                        name5 += i
                        if i.lower() != "the":
                            name7 += i

            for i in names:
                name1 += i
                if i.lower() != "the":
                    name3 += i
                if '.' in i:
                    d_names = i.split('.')
                    for j in d_names:
                        name2 += j
                else:
                    name2 += i
            movie_names.append(name1)
            name1 += "movie"
            movie_names.append(name1)
            movie_names = []
            if name2 not in movie_names:
                movie_names.append(name2)
                name2 += "movie"
                movie_names.append(name2)
            if name3 not in movie_names:
                movie_names.append(name3)
                name3 += "movie"
                movie_names.append(name3)
            if (name4 not in movie_names) and (name4 != ""):
                movie_names.append(name4)
                name4 += "movie"
                movie_names.append(name4)
            if (name5 not in movie_names) and (name5 != ""):
                movie_names.append(name5)
                name5 += "movie"
                movie_names.append(name5)
            if (name6 not in movie_names) and (name6 != ""):
                movie_names.append(name6)
                name6 += "movie"
                movie_names.append(name6)
            if (name7 not in movie_names) and (name7 != ""):
                movie_names.append(name7)
                name7 += "movie"
                movie_names.append(name7)
            x["movie_id"] = movie_id
            nam = ""
            for i in movie_names:
                nam += i + " OR "
            x["movie_name"] = row[2]
            x["list_of_mv_names"] = nam[0: -4]
            all_movie_names.append(x)
    all_movie_names_dict["data"] = all_movie_names
    txtfile()

    # movie_names.append(name1)
    # name1 += "movie"
    # movie_names.append(name1)
    # if name2 not in movie_names:
    #     movie_names.append(name2)
    #     name2 += "movie"
    #     movie_names.append(name2)
    # if name3 not in movie_names:
    #     movie_names.append(name3)
    #     name3 += "movie"
    #     movie_names.append(name3)
    # if (name4 not in movie_names) and (name4 != ""):
    #     movie_names.append(name4)
    #     name4 += "movie"
    #     movie_names.append(name4)
    # if (name5 not in movie_names) and (name5 != ""):
    #     movie_names.append(name5)
    #     name5 += "movie"
    #     movie_names.append(name5)
    # if (name6 not in movie_names) and (name6 != ""):
    #     movie_names.append(name6)
    #     name6 += "movie"
    #     movie_names.append(name6)
    # if (name7 not in movie_names) and (name7 != ""):
    #     movie_names.append(name7)
    #     name7 += "movie"
    #     movie_names.append(name7)
    # # all_movie_names[row[2]] = movie_names
    # all_movie_names[key] = movie_names
    # txtfile()


def txtfile():
    with open("tweetsv1.json", "w") as wf:
        wf.write(json.dumps(all_movie_names_dict))

    # tweets = {}
    # for key, val in all_movie_names.items():
    #     tweet = ""
    #     for item in val:
    #         tweet += item + " OR "
    #     tweets[key] = tweet[0:-4]
    # print(tweets)
    # with open("tweetsv1.json", "w") as wf:
    #     wf.write(json.dumps(tweets))


def readfile():
    with open("tweets.json", "r+") as rf:
        data = json.loads(rf.read())
        for i in data.values():
            print(i)


def writefile():
    with open("resp1.json", "w") as wf:
        wf.truncate(0)


allFilms()
# readfile()
# writefile()
