import requests
import re
from bs4 import BeautifulSoup


#function returns tag with class and id
def class_id(tag):
    return tag.has_attr('class') and tag.has_attr('id')

# create User-Agent (optional)
headers = {"User-Agent": "Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/31.0.1650.0 Safari/537.36"}
# passing the user agent as a parameter along with the get() Request
response = requests.get("http://pythonjobs.github.io/", headers=headers)
# Store the webpage contents
webpage = response.content
# Create a BeautifulSoup object out of the webpage content
soup = BeautifulSoup(webpage, "html.parser")

#find tags into list
h1_list = (soup.find_all('h1'))
lst_ = []

#finds all instances of the tages starting with a letter
for regular in soup.find_all(re.compile("^body")):
    # print(regular)
    # print(vars(regular))
    lst_.append(regular.name)
    # print(regular.name)

#finds all <a> and <i> tags
for tag in soup.find_all(['a', 'i']):
    print(tag)

print('\r\n----------------------------------\r\n')


#find tags using function: lookup for tags with class and id
for tag in soup.find_all(class_id):
    print(tag)

print('\r\n----------------------------------\r\n')

#find the first occurance
print(soup.find('h1'), type(soup.find('h1')), soup.find('a'), "\n")

#find tag with id or with class
print(soup.find('div',id='search_info'))
print(soup.find('i',attrs={'class': 'i-globe'}))

#-------------------------------using find_all----------find_all---------find_all-------find_all--------

#find a tag with class and place it into list
#allows to filter seach with multiple attrs :TODO (how to use reqexp or wildcards here???)
print(soup.find_all('i', class_='i-github'))
print(soup.find_all('a', attrs={'class': 'about', 'href': 'https://www.github.com/pythonjobs/jobs'})) 

#The string argument allows us to search for strings instead of tags.
print(soup.find_all(string=["Python", "Java", "Golang"]))

#finds only the first two tags
print(soup.find_all("a", limit=2))


# The logic
for job in soup.find_all('section', class_='job_list'):
    title = [a for a in job.find_all('h1')]
    for n, tag in enumerate(job.find_all('div', class_='job')):
        company_element = [x for x in tag.find_all('span', class_='info')]
        print("Job Title: ", title[n].text.strip())
        print("Location: ", company_element[0].text.strip())
        print("Company: ", company_element[3].text.strip())
        print()


print(response.status_code)
# print(webpage)
print(h1_list[0])
print(lst_)

