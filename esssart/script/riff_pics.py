import requests
import json
import os
from .. import endlesss_auth


def request_riffs(limit, start):
    try:
        response = requests.get(
            url="https://api.endlesss.fm/rifff-feed/query",
            params={
                "skip": start,
                "limit": limit,
                "following": "true",
            },
            headers={
                "Host": "api.endlesss.fm",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Cookie": "LB=live02",
                "User-Agent": "Endlesss/0 CFNetwork/1331.0.7 Darwin/21.4.0",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                *endlesss_auth,
        },
        )
        print(
            "Response HTTP Status Code: {status_code}".format(
                status_code=response.status_code
            )
        )
        if response.status_code == 200:
            file_path = 'data/json/endlesss.myfollowedrifffs.json'
            new_data = response.json().get("data", [])

            # Open file in append mode and write new data
            with open(file_path, 'a') as json_file:
                for entry in new_data:
                    json_file.write(json.dumps(entry) + '\n')
        else:
            print("Failed to retrieve data")
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed: {error}".format(error=str(e)))


def request_liked_riffs(limit, start):
    try:
        response = requests.get(
            url="https://api.endlesss.fm/api/v3/feed/likedByMe",
            params={
                "from": start,
                "size": limit
            },
            headers={
                "Host": "api.endlesss.fm",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Cookie": "LB=live02",
                "User-Agent": "Endlesss/0 CFNetwork/1331.0.7 Darwin/21.4.0",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                *endlesss_auth,
            },
        )
        print(
            "Response HTTP Status Code: {status_code}".format(
                status_code=response.status_code
            )
        )
        if response.status_code == 200:
            file_path = 'data/json/endlesss.mylikedrifffs.json'
            new_data = response.json().get("data", [])

            # Open file in append mode and write new data
            with open(file_path,                                'a') as json_file:
                for entry in new_data:
                    json_file.write(json.dumps(entry) + '\n')
        else:
            print("Failed to retrieve data")
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed: {error}".format(error=str(e)))
