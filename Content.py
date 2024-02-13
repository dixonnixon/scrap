import requests
from bs4 import BeautifulSoup
import re


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body
        
def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')

def scrapeNYTimes(url):
    bs = getPage(url)
    title = bs.find("h1").text
    lines = bs.find_all("p", {"class":"story-content"})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


def scrapeBrookings(url):
    bs = getPage(url)
    target_list = []
    """!!!Find matcing classes"""
    for tag in bs.find_all("div"):
        if tag.has_attr('class'):
            # print("classes",tag.get_attribute_list('class'))
            classes = tag.get_attribute_list('class')
            matches = [match for match in classes if "post" in match]
            if len(matches) > 0:
                target_list.append(tag)

            # print(tag, no_list_soup)
    # print(bs.find("h1").parent)
    title = bs.find("h1").text.strip()
    body = bs.find("div", {"class", "wysiwyg"}).text.strip()
    return Content(url, title, body)


url = 'https://www.brookings.edu/blog/future-development'
'/2018/01/26/delivering-inclusive-urban-access-3-unc'
'omfortable-truths/'
content = scrapeBrookings(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)
url = 'https://www.nytimes.com/2018/01/25/opinion/sunday/'