from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
# import requests_cache
import datetime
import re
import random
import time

random.seed(str(datetime.datetime.now()))
# requests_cache.install_cache()

url = 'http://en.wikipedia.org{}'

def getLinks(articleUrl):
    session = requests.Session()
    # response = requests.get('http://en.wikipedia.org/wiki/Kevin_Bacon')
    response = session.get(url.format(articleUrl))
    print(response)
    if response.status_code == 200:
        html = response.content

        bs = BeautifulSoup(html, 'html.parser')
        try:
            id_content = bs.find('div', {'id':'bodyContent'})
            return id_content.find_all(
                'a', href = re.compile('^(/wiki/)((?!:).)*$'))
        except AttributeError:
            print('No such Id')
            return []

    # print(session)
                
links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    time.sleep(3)
    links = getLinks(newArticle)