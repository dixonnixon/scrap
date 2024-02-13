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

# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()
internalLimit = 0


#Retrieves a list of all Internal links found on a page
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,
    urlparse(includeUrl).netloc)
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bs.find_all('a',
        href=re.compile('^(/|.*'+includeUrl+')')):
        # print(link)
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/') 
                    ):
                    
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
        # print(link)
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
                # return externalLinks
    return externalLinks


def checkHead(stringUrl):
    print(stringUrl)
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
    headers = {"User-Agent": "Talos"} 

    try:
        req = urllib.request.Request(stringUrl, method="HEAD", headers=headers)
        resp = urllib.request.urlopen(req)
        # print('\r\n head=',  type(resp),
        #     resp.headers, '\n', 'headers[]= ', resp.getheaders(), '\n',
        #     'url = ', resp.url, 'info= ', resp.info, 'status=', resp.status)

        if resp.status == 200:
            return True
        
    except HTTPError as e:
        print("Head req error: ",e, e.read().decode()) 
    except  e:
        print('unknown error!', e)
    
    return False


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
    # print(type(externalLinks))

    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(startingPage).scheme,
        urlparse(startingPage).netloc)
        print("domain=", domain)
        internalLinks = getInternalLinks(bs, domain)
        link = internalLinks[random.randint(0,
            len(internalLinks)-1)]
        return getRandomExternalLink(link)
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]



def getAllExternalLinks(siteUrl):
    '''Getting external links from target web resource'''
    html = urlopen(siteUrl)
    domain = '{}://{}'.format(urlparse(siteUrl).scheme,
    urlparse(siteUrl).netloc)
    bs = BeautifulSoup(html, 'html.parser')
    internalLinks = getInternalLinks(bs, domain) #^/
    externalLinks = getExternalLinks(bs, domain) #^http|www
    print('\r\n\n Gathered internal: \n',  len(allIntLinks), allIntLinks)
    print('\r\n Scraped internal: ', len(internalLinks), internalLinks)
    print('\r\n Scraped ext: ', len(externalLinks), externalLinks)
    print('\n--------------------------------------\n')
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            # print(link)
    
    print(enumerate(internalLinks), len(internalLinks))
    #this would be performed until the end of unique links of the last scrped page
    limit = internalLimit or len(internalLinks)
    # distinct = []
    for num, link in enumerate(internalLinks): 
        print(num, num < limit, link)
        if link not in allIntLinks:
            # distinct.append(link)
            allIntLinks.add(link)
            print('\r\nnext link', link, num, '\n\n')
            if num < limit:
                getAllExternalLinks(link)

    # print(len(distinct))
    print(len(allIntLinks), len(allExtLinks))
    # print('\n--------------------------------\n')


def followExternalOnly(startingSite):
    print(checkHead(startingSite))
    if checkHead(startingSite):
        externalLink = getRandomExternalLink(startingSite)
        print('Random external link is: {}'.format(externalLink))


        followExternalOnly(externalLink)
    return 0




try:
    followExternalOnly('http://oreilly.com')
    followExternalOnly('https://channelstore.roku.com/')
    # allIntLinks.add('http://oreilly.com')
    # getAllExternalLinks('http://oreilly.com')

except KeyboardInterrupt:
    print("The end by cli")

