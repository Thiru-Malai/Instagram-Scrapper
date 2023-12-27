import subprocess
import main 
import re

def extract_video_id(url):
    if '?' in url:
        url = url.split('?')[0] + '/'
    pattern = r'/(\d+)/'
    match = re.search(pattern, url)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None

with open('instagram.txt', 'r') as file:
    for line in file:
        video_id = extract_video_id(line)
        if video_id is not None:
            print(video_id)
            subprocess.call(['python', 'main.py', video_id])