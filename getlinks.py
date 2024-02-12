from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
invalid = set()

def getLinks(pageUrl):
    global pages
    url = 'http://en.wikipedia.org{}'.format(pageUrl)
    try:
        html = urlopen(url)
    except:
        print("sd")
        html = ''
        invalid.add(url)
    bs = BeautifulSoup(html, 'html.parser')

    try:
        print(bs.h1.get_text())
        print(bs.find(id ='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span')
        .find('a').attrs['href'])
    except IndexError:
        print('This content is missing something! Continuing.')
    except AttributeError:
        print('This page is missing something! Continuing.')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
            #We have encountered a new page
                newPage = link.attrs['href']
                print("\r\n", url, newPage, pages, invalid)
                pages.add(newPage)
                getLinks(newPage)

getLinks('')