import argparse
import requests
from urllib.parse import quote_plus
from json import dumps, decoder


def getUserId(username,sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96'}
    api = requests.get(
        f'https://www.instagram.com/{username}/?__a=1&__d=dis',
        headers=headers,
        cookies=cookies
    )
    try:
        if api.status_code == 404:
            return {"id": None, "error": "User not found"}
        
        id = api.json()["logging_page_id"].strip("profilePage_")
        return {"id":id, "error": None}

    except decoder.JSONDecodeError:
        return {"id":None, "error":"Rate limit"}

def getInfo(username,sessionId):
    userId = getUserId(username, sessionId)
    if userId["error"]:
        return userId

    response = requests.get(
        f'https://i.instagram.com/api/v1/users/{userId["id"]}/info/',
        headers={'User-Agent': 'Instagram 64.0.0.14.96'},
        cookies={'sessionid': sessionId}
    ).json()["user"]
    
    infoUser = response
    infoUser["userID"] = userId["id"]
    
    return {"user":infoUser, "error":None}

def advanced_lookup(username):
    """
        Post to get obfuscated login infos
    """
    data = "signed_body=SIGNATURE."+quote_plus(dumps(
        {"q":username, "skip_recovery":"1"},
        separators=(",",":")
    ))
    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            #"X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    try:
        return({"user": api.json(),"error": None})
    except decoder.JSONDecodeError:
        return({"user": None, "error": "rate limit"})

def main(username, sessionId):
    infos = getInfo(username, sessionId)
    if not infos["user"]:
        exit(infos["error"])

    infos=infos["user"]
 
    # other_infos=advanced_lookup('gunas___bond___007')
    
    return infos