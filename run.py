import subprocess
import main 
import re

def extract_audio_ids(url):
    match = re.search(r'/audio/(\d+)', url)
    if match:
        audio_id = match.group(1)
    return audio_id

with open('instagram.txt', 'r') as file:
    for line in file:
        video_id = extract_audio_ids(line)
        if video_id is not None:
            print(video_id)
            subprocess.call(['python', 'main.py', video_id])