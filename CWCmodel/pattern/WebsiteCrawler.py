import requests
from bs4 import BeautifulSoup
from content import Content
from website import Website
# from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
from pathlib import Path
import asyncio

import re

#not tested but should work

'''
    This type of crawler works well for projects when you want to gather all the data from
        a site—not just data from a specific search result or page listing. It also works well
        when the site`s pages may be disorganized or widely dispersed.
'''

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []
    
    def getPage(self, url): #pretty cool) 
        try:
           
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded")

                # Wait for the page to load fully
                page.wait_for_timeout(5000)
                page.wait_for_selector
                # Now you can access the full content of the page, including any dynamic content loaded by JavaScript
                html = page.content()

                page.wait_for_timeout(1000)


                browser.close()
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(html, 'html.parser')
    
    def safeGet(self, pageObj, selector): #almost good
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for
                elem in selectedElems])
        return ''
    
    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            print(title, body)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()
        else: print('bs is null')

    def crawl(self):
        """
        Get pages from website home page
        """
        bs = self.getPage(self.site.url)
        targetPages = bs.findAll('a',
            href=re.compile(self.site.targetPattern))
        print(bs.prettify(), targetPages, self.site.targetPattern, self.site.url)
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                self.parse(targetPage)

reuters = Website('Reuters', 'https://www.reuters.com/news/', '^(/article/)', False,
'h1', 'div.StandardArticleBody_body_1gnLA')
crawler = Crawler(reuters)
crawler.crawl()