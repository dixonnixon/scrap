from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getNgrams(content, n):
  content = re.sub('\n|[[\d+\]]', ' ', content)
  content = bytes(content, 'UTF-8')
  content = content.decode('ascii', 'ignore')
  content = content.split(' ')
  content = [word for word in content if word != '']
  output = []
  for i in range(len(content)-n+1):
    if i < 100:
      print(i, i+n, content[i:i+n])
    output.append(content[i:i+n])
  return output

html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
bs = BeautifulSoup(html, 'html.parser')
content = bs.find('div', {'id':'mw-content-text'}).get_text()
ngrams = getNgrams(content, 2)
# print(ngrams)
print('2-grams count is: '+str(len(ngrams)))
