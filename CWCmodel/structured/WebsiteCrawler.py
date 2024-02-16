import requests
from bs4 import BeautifulSoup
from content import Content
from website import Website
from playwright.sync_api import sync_playwright
from pathlib import Path


'''
    use single string CSS selector for each piece of info
    and put it in a dict...


    Using these Content and Website classes you can then write a Crawler to scrape the
    title and content of any URL that is provided for a given web page from a given web
    site

    Crawling over a topics sequentiallu one article topic by one site 
        and not all articles from the site    
'''

class Crawler:

    def getStaticUrl(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
    
    def getPage(self, url): #pretty cool) 
        try:
           
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)

                # Wait for the page to load fully
                page.wait_for_timeout(1000)

                # Now you can access the full content of the page, including any dynamic content loaded by JavaScript
                html = page.content()

                with open(str(Path.cwd()) + "/CWCmodel/data/dyn.txt", "w") as file1:
                    # Writing data to a file
                    file1.write(html)

                # print(html)

                browser.close()
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(html, 'html.parser')
    
    def safeGet(self, pageObj, selector): #almost good
        """
        Utility function used to get a content string from a
        Beautiful Soup object and a selector. Returns an empty
        string if no object is found for the given selector
        """
        # selectedElems = pageObj.select(selector)
        # if selectedElems is not None and len(selectedElems) > 0:
        #     return '\n'.join(
        #         [elem.get_text() for elem in selectedElems])
        # return ''
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ""
    
    # def parse(self, site, url):
    #     """
    #     Extract content from a given page URL
    #     """
    #     bs = self.getPage(url)
    #     if bs is not None:
    #         title = self.safeGet(bs, site.titleTag)
    #         body = self.safeGet(bs, site.bodyTag)
    #     if title != '' and body != '':
    #         content = Content(url, title, body)
    #         content.print()
    def search(self, topic, site):
        """
        Searches a given website for a given topic and records all pages found
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        # print('search', len(searchResults))
        for num, result in enumerate(searchResults):
            url = result.select(site.resultUrl)[num].attrs["href"]
            # print(type(result),   site.resultUrl, '\n\n\n', result.select(site.resultUrl)[0],
            #     url)
            # # Check to see whether it's a relative or an absolute URL
            if(site.absoluteUrl):
                bs = self.getStaticUrl(url)
            else:
                bs = self.getStaticUrl(site.url + url)

            if bs is None:
                print("Something was wrong with that page or URL. Skipping!")
                return
            
          
            title = self.safeGet(bs, site.titleTag)
            
            body = self.safeGet(bs, site.bodyTag)
            # print(body, title)
            
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()
            else:
                print("Empty Title & body?")

crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com',
        # 'https://www.oreilly.com/search/?q=','article.product-result',
        'https://www.oreilly.com/search/?q=','div#search-main-content >  section',
        'article a', True, 'h3', 'div.content > span'],
    ['Reuters', 'http://reuters.com',
        'http://www.reuters.com/search/news?blob=',
        'div.search-result-content','h3.search-result-title a',
        False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
        'https://www.brookings.edu/search/?s=',
        'div.list-content article', 'h4.title a', True, 'h1',
        'div.post-body']
]
sites = []
# name, url, searchUrl, resultListing,
        # resultUrl, absoluteUrl, titleTag, bodyTag
for row in siteData:
    sites.append(Website(row[0], row[1], row[2],
        row[3], row[4], row[5], row[6], row[7]))

print(repr(sites[0]))

topics = ['python', 'data+science']
for topic in topics:
    print("GETTING INFO ABOUT: " + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)