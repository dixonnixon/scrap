import requests
from bs4 import BeautifulSoup
import vimeo

from content import Content
import base64
from playwright.sync_api import sync_playwright
from pathlib import Path
import webvtt
from dotenv import load_dotenv

from moviepy.editor import *
import speech_recognition as sr

import os
import json

load_dotenv()
# 915051800/baf3fdcde5') 

def with_token(token):
    def get_data(video_id):
        headers = {
          "Authorization": f"Bearer {token}",
          "Accept": "application/vnd.vimeo.*+json;version=3.4"
        }
        print(headers, video_id)

        try:
          req = requests.get(f"https://api.vimeo.com/videos/{video_id}",
            headers = headers
          )
          
        except requests.exceptions.RequestException as e:
          print(e)
          print(res)
          return None
        res = req.json()
        print(req.status_code)
        # Use token to access data from url
        pass
    return get_data


def getToken(client_id, client_secret):
  authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")
  headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.vimeo.*+json;version=3.4"
  }

  body = {
    "grant_type": "client_credentials",
    "scope": "public"
  } 

  try:
    req = requests.post('https://api.vimeo.com/oauth/authorize/client',
      headers = headers,
      json=body
    )
  except requests.exceptions.RequestException as e:
    print(e)
    return None
  res = req.json()
  return res['access_token']


def mp4towav(mp4file, wavfile):
    videoclip=VideoFileClip(mp4file)
    audioclip=videoclip.audio
    audioclip.write_audiofile(wavfile,codec='pcm_s16le')
    audioclip.close()
    videoclip.close()

save_track = with_token(getToken(
  os.getenv('VIMEO_CLIENT_ID'),
  os.getenv('VIMEO_CLIENT_SECRET')
))

target_quality = '360p'
video_id = 355336541

client = vimeo.VimeoClient(
  token='VIMEO_ACCESS',
  key='VIMEO_CLIENT_ID',
  secret='VIMEO_CLIENT_SECRET'
)

response = client.get('https://player.vimeo.com/video/' + str(video_id) + '/config')

files = response.json()['request']['files']['progressive']

for file in files:
  if file['quality'] == target_quality:
    video_url = file['url']
    video_name = str(video_id) + '_' + file['quality'] + '.mp4'
    video_response = requests.get(video_url)

    video_file = open(video_name, 'wb')
    video_file.write(video_response.content)
    video_file.close()

    # print('downloaded: ' + video_name)
    mp4towav(video_name,"audio.wav")

r = sr.Recognizer()
comments = sr.AudioFile('audio.wav')
with comments as source:
  audio = r.record(source)
  text = r.recognize_google(audio)
  print(text)



def getTextfromVideo():
  #try load dynamic
  target_link = None

  with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://vimeo.com/915051800/baf3fdcde5')
    page.wait_for_load_state()
    page.wait_for_timeout(8000)
    page.wait_for_timeout(8000)
    
    html = page.content()
    bs = BeautifulSoup(html, 'html.parser')
    track = bs.select("track")
    target_link = "https://vimeo.com" + track[0]['src']
    print(track[0]['src'])
    

    # sometime later...
    page.wait_for_timeout(8000)
    # page.remove_listener("request", handle_request)
    # page.remove_listener("request", load_tracker)
    browser.close()

  if target_link:
    headers = {
      "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) \
          AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 \
          Safari/9537.53"
    }

    print('requesting ', target_link)
    try:
      req = requests.get(target_link, headers=headers)
    except requests.exceptions.RequestException as e:
      print(e)

    with open(str(Path.cwd()) + "/text.vtt", "w") as file1:
      # Writing data to a file
      file1.write(req.text)

    out_text = ""
    for caption in webvtt.read(str(Path.cwd()) + "/text.vtt"):
      out_text += caption.text
      print(caption.text)

    with open(str(Path.cwd()) + "/text.txt", "w") as file2:
      # Writing data to a file
      file2.write(out_text)

