from playwright.sync_api import sync_playwright
import json
from time import sleep

SESSIONID = "63694293363:UQdy1oqqybUDUq:11:AYe50Zx0LGJfnW4y-zEYpfvFkZSPMdv2QaT5OVRSjQ"
headers = { 
  "cookie":f'sessionid={SESSIONID};'
}

j = json.loads('{}')
res = []
index = 1
totalCount = 0

def check(response):
    if "music" in response.url:
      data = response.json()

      global index, totalCount
      index = len(data['items'])
      if(index == 0):
        exit()
      totalCount = totalCount + index
      print('Total Count', totalCount)
      print(len(data['items']))

      for i in range(index): 
        code = data['items'][i]['media']["code"]
        username = data['items'][i]['media']["owner"]["username"]
        profile = "https://www.instagram.com/"+username
        reel = "https://www.instagram.com/reel/"+code
        value = []
        value.append(username)
        value.append(profile)
        value.append(reel)
        if value not in res:
          res.append(value)
      json.dump(res,open("result.json", "w"))
      # sleep(1)
      
      # try:
      # j.update(response.json())
      # except:
      #   print("error")
      #   return

with sync_playwright() as p:
  browser = p.firefox.launch(headless=False)
  page = browser.new_page(extra_http_headers=headers)
  page.on("response", lambda response: check(response))
  
  page.goto("https://www.instagram.com/reels/audio/1088122805511195/")
  sleep(2)
  # page.wait_for_timeout(2000)
  page.wait_for_load_state("networkidle")
  

  while True:

    page.mouse.wheel(0, -2)
    page.mouse.wheel(0, 20000)
    sleep(2)