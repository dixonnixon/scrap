import requests
from bs4 import BeautifulSoup
from content import Content
import base64
from playwright.sync_api import sync_playwright
from pathlib import Path
import webvtt
from dotenv import load_dotenv


import os
import json

load_dotenv()

# from requests_html import AsyncHTMLSession
# import asyncio

# from requests_html import HTMLSession

# OAuth Redirect Authentication: https://api.vimeo.com/oauth/authorize
# Access token URL: https://api.vimeo.com/oauth/access_token
# token: e64ec5b8403d282a1c29f896ac958c96

# [ ] make an IP call to check if titles in a video 

# r = requests.get('https://vimeo.com/915051800/baf3fdcde5')  # replace '<URL>' with the URL of the webpage

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


def getTextTrackUri(video_id):
  headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) \
        AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 \
        Safari/9537.53",
    "Authorization": "bearer e64ec5b8403d282a1c29f896ac958c96",
    "Accept": "application/vnd.vimeo.*+json;version=3.4"
  }
  link = 'https://api.vimeo.com/videos/{}'.format(video_id)
  print('requesting ', link)
  try:
    req = requests.get(link, headers=headers)
  except requests.exceptions.RequestException as e:
    print(e)
    return None
  return req.text


# Use '.html' method to parse the HTML
# token = getToken("719a17658560fd1305db6f452897b8ad9661e228",
#   "NUDOOuCpGE+eOqdXQfkrb1Ea4v5i3Yrhs3pqX0HH375GAX3gcVsoG0VkUXxcSUQej0zMQMzOCqxCA2iO8KYQo4lekMh49sqhzSzMulFMa/hfMyZiDDb/cpffPSkHq1e1"
# )

# if token:
#   print(token)

get_track = with_token(getToken(
  os.getenv('VIMEO_CLIENT_ID'),
  os.getenv('VIMEO_CLIENT_SECRET')
))

print(get_track(915051800))

def getTextfromVideo():
  #try load dynamic
  target_link = None

  with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    # page.goto('http://pythonscraping.com/pages/javascript/redirectDemo1.html')
    page.goto('https://vimeo.com/915051800/baf3fdcde5')
    # page.goto('https://vimeo.com/bestoftheyear')
    # print(page.wait_for_load_state())
    page.wait_for_load_state()
    page.wait_for_timeout(8000)
    # page.on("load", load_tracker)
    # page.on('request', handle_request)
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

