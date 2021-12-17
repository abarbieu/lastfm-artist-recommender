import requests
import numpy as np
import re
import json
import time
import pandas as pd
from collections import deque
from bs4 import BeautifulSoup

API_KEY=None
USER_AGENT=None
PASSWORD=None
with open("./secrets.txt", "r") as s:
    lines = s.readlines()
    API_KEY = lines[0].strip("\n")
    USER_AGENT = lines[1].strip("\n")
    PASSWORD = lines[2].strip("\n")
    

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

if __name__ == "__main__":
    client = requests.Session()

    users = pd.read_csv("./udata/usernames.csv", header=None)[0].to_numpy()
    #     artistids = pd.read_csv("./udata/artists.csv", header=None)[0].to_numpy()
    artists = []

    ftop = open("./udata/10000users_200listens.csv", "a", encoding="utf-8")
    faid = open('./udata/artists.csv', "a", encoding="utf-8")

    uid=0
    while uid < 10000:
    #         print(f"fetching {userids[uid]} w new uid {uid}")
        payload = {
            "method": "user.gettopartists",
            "user": users[uid],
            "period": "overall",
            "limit": 200
        }
        try:
            r = lastfm_get(payload)
            j = r.json()
            if "topartists" in j and "artist" in j["topartists"]:
                listens = r.json()['topartists']["artist"]
                for a in listens:
                    if a['name'] not in artists:
                        artists = np.append(artists, a['name'])
                        faid.write(f"{a['name']}\n")
                    ftop.write(f"{uid},{np.where(artists == a['name'])[0][0]},{int(a['playcount'])}\n")
        except Exception as e:
            print(e)
            uid -= 1
        uid += 1
    ftop.close()
    faid.close()
