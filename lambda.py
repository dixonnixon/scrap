from bs4 import Comment
from bs4 import Tag
from bs4 import NavigableString
from bs4 import BeautifulSoup
import requests

url = "https://tomordonez.com/python-lambda-beautifulsoup/"
response = requests.get(url)
if response.status_code == 200:
    """Find Commnets"""
    soup = BeautifulSoup(response.content, "html.parser")
    #!
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    print(comments)

    nav = soup.find_all(string=lambda text: isinstance(text, NavigableString))
    for lno, line in enumerate(nav):
        if len(line) < 75 and line:
            print(lno, line, type(line))

    twoattr = soup.find_all(lambda tag: len(tag.attrs) == 4)
    print(twoattr)