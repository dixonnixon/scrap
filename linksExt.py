from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request
import urllib.request

from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(str(datetime.datetime.now()))

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,
    urlparse(includeUrl).netloc)
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bs.find_all('a',
        href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(
                    includeUrl+link.attrs['href'])
        else:
            internalLinks.append(link.attrs['href'])
            return internalLinks
        
#Retrieves a list of all external links found on a page
def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" that do
    #not contain the current URL
    for link in bs.find_all('a',
        href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        print(link)
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
                # return externalLinks
    return externalLinks


def getRandomExternalLink(startingPage):
    print(startingPage)

    req = Request(
        startingPage, 
        data=None, 
        headers={
            'User-Agent': 'curl/8.3.0'
        }
    )


   
    try:
        # html = urlopen(startingPage)
        html = urllib.request.urlopen(req)
        # print(html.read().decode('utf-8'))
    except HTTPError as e:
        print(e, e.read().decode()) 

    # print(html.read())

    bs = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bs,
        urlparse(startingPage).netloc)
    print(externalLinks, type(externalLinks))
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(startingPage).scheme,
        urlparse(startingPage).netloc)
        print("domain=", domain)
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0,
        len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('Random external link is: {}'.format(externalLink))


    followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')

