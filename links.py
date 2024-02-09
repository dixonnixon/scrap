from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import requests_cache
import re

requests_cache.install_cache()
session = requests.Session()
url = 'http://en.wikipedia.org/wiki/Kevin_Bacon'
# response = requests.get(url)
response = session.get(url)

if response.status_code == 200:
    html = response.content

    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('div', {'id':'bodyContent'}).find_all(
        'a', href = re.compile('^(/wiki/)((?!:).)*$')):
        print(link)
        if 'href' in link.attrs:
            print(link.attrs['href'])

    # print(session)