import requests
import json
from time import sleep
import numpy
import sys
from Getuserdata import main
from datetime import datetime


#api
url = "https://www.instagram.com/api/v1/clips/music/"

# global variables
# video_id = "1322610878461284"
sessionId = "63694293363:BX18ThrpjBmExz:29:AYcHshaGNwKZ6LHzMB61bLjcmyvZ9K4k7VuWKRCabw"
csrftoken = "TCxi1uzVXDDkMfBLVRgbg88yP8COEUvL"

max_id = ""
next_available = True
total = 0
last_length = 1
json_data = {}
v_count = 0

headers = {
    "X-Asbd-Id": "129477",
    "X-Csrftoken": csrftoken,
    "X-Ig-App-Id": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": f"csrftoken={csrftoken};sessionid={sessionId};",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Parsing Data
def getData(reels_data, filepath, filename):
    result = []
    for i in range(len(reels_data['items'])):
        username = reels_data['items'][i]['media']["owner"]["username"]
        code = reels_data['items'][i]['media']["code"]
        date = reels_data['items'][i]['media']['taken_at']
        datetime_obj = datetime.fromtimestamp(date)
        # Profile Scrapping
        data = {}
        infos = main(username, sessionId)
        
        data["username"] = username
        data["reelsUrl"] = "https://www.instagram.com/reel/"+code
        data["upload_date"] = str(datetime_obj)
        data["followers"] = infos["follower_count"]
        data["following_count"] = infos["following_count"]
        data["postsCount"] = infos["media_count"]
        if infos["external_url"]:
            data["profileUrl"] = infos["external_url"]
        if "public_email" in infos.keys():
            if infos["public_email"]:
                data["descEmail"] = infos["public_email"]
            else:
                data["descEmail"] = "Null"
        result.append(data)

        sleep(4.0 + numpy.random.uniform(0,3))

    with open(filepath, "r") as file:
        json_data = json.load(file)
        json_data['userDetails'].extend(result)
        json.dump(json_data,open(filename, "w"))


def main_process(video_id):
    filename = video_id + ".json"
    filepath = './' + filename
    
    # main

    global max_id, next_available, total, last_length, json_data, v_count
    json_data['userDetails'] = []
    json.dump(json_data,open(filename, "w"))

    while next_available and last_length > 0:
        data = f'audio_cluster_id={video_id}&original_sound_audio_asset_id={video_id}&max_id={max_id}'
        response = requests.post(url, headers=headers, data=data)
        print(response)
        if(response.status_code == 400):
            print("Error 400")
            sleep(60 + numpy.random.uniform(6, 12))
            pass
        else:
            res = response.json()
            v_count = res['media_count']["clips_count"]
            next_available = res["paging_info"]["more_available"]
            max_id = res["paging_info"]["max_id"]
            last_length = len(res['items'])
            total += len(res['items'])
            print(total)
            getData(res, filepath, filename)
            sleep(6.0 + numpy.random.uniform(4,20))
        
    with open(filepath, "r") as file:
        json_data = json.load(file)
        json_data['totalClips'] = v_count
        json.dump(json_data,open(filename, "w"))

    sleep(60 + numpy.random.uniform(4, 16))

if len(sys.argv) > 1:
    video_id = sys.argv[1]
    main_process(video_id)
