import requests
import json
from time import sleep
import numpy
import sys
from Getuserdata import main
from datetime import datetime
import re
import random
import os

#api
url = "https://www.instagram.com/api/v1/clips/music/"
profile_api1 = "https://www.instagram.com/api/v1/users/web_profile_info/?username="
profile_api2 = "https://www.instagram.com/api/v1/users/"

profile=[profile_api1, profile_api2]

# global variables
sessionId = "63694293363%3AXY2kJYJqroXpDO%3A0%3AAYe-WPmQ_qkvuYLDbRZfF-7zTrGBXf7ybAnNVnnTpQ"
csrftoken = "9IUoNSjuveFtHRETUyx8CjThsGzpsroR"

headers_profile = {
    "X-Asbd-Id": "129477",
    "X-Csrftoken": csrftoken,
    "X-Ig-App-Id": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": f"csrftoken={csrftoken};sessionid={sessionId};ds_user_id=63694293363;rur='NHA\05463694293363\0541735293082:01f72ea1a8a68ac0c86286125881d513559a5bea5c17a18a84045df175ae5483d891af6b;mid=X9Z8jwALAAH5Z9Z1X9Z8jwALAAH5Z9Z1';ig_did=A54AE8B0-10AF-4070-8D2E-EC53FCB11131; csrftoken=9IUoNSjuveFtHRETUyx8CjThsGzpsroR;",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

proxy_list = ['134.209.29.120:8080', '13.229.92.153:8888', '34.81.72.31:80', '139.162.78.109:3128', '139.59.1.14:8080', '188.166.56.246:80']

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
    global profile
    for i in range(len(reels_data['items'])):
        user_id = 0
        followers = 0
        following = 0
        external_url = ''
        bio = ''
        descEmail = ''
        post_count = 0
        
        
        username = reels_data['items'][i]['media']["owner"]["username"]
        user_id= reels_data['items'][i]['media']["owner"]["id"]
        code = reels_data['items'][i]['media']["code"]
        date = reels_data['items'][i]['media']['taken_at']
        datetime_obj = datetime.fromtimestamp(date)
        profile = "https://www.instagram.com/"+username
        reel = "https://www.instagram.com/reel/"+code   
           
        data = {}        
        profile_data = {}
        
        # Profile Scrapping
        payload = f"username={username}"
        profile_api = random.choice(profile)
        if(profile_api == profile_api1):
            profile_api = profile_api1 + username
        else:
            profile_api = profile_api2 + user_id + "/info/"
            profile_data['data'] = {}
        
        profile_response = requests.get(profile_api, headers=headers_profile, data=payload, proxies={'http': f"http://{random.choice(proxy_list)}"})

        if(profile_response.status_code == 400):
            print("Error 400")
            sleep(120 + numpy.random.uniform(6, 12))
            pass
        if(profile_response.status_code == 429):
            print("Error 429 Too Many Requests")
            sleep(120 + numpy.random.uniform(6, 12))
            pass
        
        if('info' in profile_api and profile_response.status_code == 200):
            profile_data['data'] = profile_response.json()
            user_id = profile_data['data']['user']['pk']
            followers = profile_data['data']['user']['follower_count']
            following = profile_data['data']['user']['following_count']
            external_url = profile_data['data']['user']['external_url']
            bio = profile_data['data']['user']['biography']
            descEmail = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", bio)
            post_count = profile_data['data']['user']['media_count']
     
        else:
            profile_data = profile_response.json()
            user_id = profile_data['data']['user']['id']
            followers = profile_data['data']['user']['edge_followed_by']['count']
            following = profile_data['data']['user']['edge_follow']['count']
            external_url = profile_data['data']['user']['external_url']
            bio = profile_data['data']['user']['biography']
            descEmail = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", bio)
            post_count = profile_data['data']['user']['edge_owner_to_timeline_media']['count']

        data["username"] = username
        data['id'] = user_id
        data["reelsUrl"] = reel
        data["profileUrl"] = profile
        data["followers_count"] = followers
        data['following_count'] = following
        data["externalUrl"] = external_url
        data['bio'] = bio
        data["descEmail"] = descEmail
        data["postsCount"] = post_count
        data["upload_date"] = str(datetime_obj)
        
        result.append(data)

        sleep(5.0 + numpy.random.uniform(2,10))

    with open(filepath, "r") as file:
        json_data = json.load(file)
        json_data['userDetails'].extend(result)
        json.dump(json_data,open(filename, "w"))


def main_process(video_id):
    filename = video_id + ".json"
    filepath = './' + filename
    
    # main
    j = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            j = json.load(file)

    global max_id, next_available, total, last_length, json_data, v_count
    json_data['userDetails'] = []
    json.dump(json_data,open(filename, "w"))

    while next_available and last_length > 0:
        data = f'audio_cluster_id={video_id}&original_sound_audio_asset_id={video_id}&max_id={max_id}'
        response = requests.post(url, headers=headers, data=data, proxies={'http': f"http://{random.choice(proxy_list)}"})
        print(response)
        if(response.status_code == 400):
            print("Error 400")
            sleep(60 + numpy.random.uniform(6, 12))
            pass
        if(response.status_code == 429):
            json.dump(json_data,open(j, "w"))
            print("Error 429 Too Many Requests")
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
            sleep(12.0 + numpy.random.uniform(4,20))
        
    with open(filepath, "r") as file:
        json_data = json.load(file)
        json_data['totalClips'] = v_count
        json.dump(json_data,open(filename, "w"))

    sleep(60 + numpy.random.uniform(10, 30))

if len(sys.argv) > 1:
    video_id = sys.argv[1]
    main_process(video_id)
