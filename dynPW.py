from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import json

"""
Goal:
  After this is done, the second webdriver should have the same cookies as the first.
  According to Google Analytics, this second webdriver is now identical to the first
  one, and they will be tracked in the same way. If the first webdriver was logged into a
  site, the second webdriver will be as well.
"""

folder_data = Path.cwd() / 'data' 
filename = str(folder_data) + '/state.json'

with sync_playwright() as p:
  browser = p.chromium.launch()
  browser_add = p.chromium.launch()
  # page = browser.new_page()


  context = browser.new_context()

  context = browser_add.new_context()

  page = context.new_page()
  # page.goto('http://pythonscraping.com/pages/javascript/redirectDemo1.html')
  page.goto('http://ukr.net')

  # Wait for the page to load fully
  page.wait_for_timeout(1000)
  # Save storage state into the file.
  with open(filename, 'w') as file:
    storage = context.storage_state(path='data/state.json')
    # Create a new context with the saved storage state.
    
    # json.dump([], filename)
    context = browser.new_context(storage_state=filename)
    # context.add_cookies([{'name': 'Accept:', 'value': 'All'}])

    savedCookies = context.cookies()
    context.clear_cookies()

    
    print(len(savedCookies), type(savedCookies))

    session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
    os.environ["SESSION_STORAGE"] = session_storage


    # Set session storage in a new context
    session_storage = os.environ["SESSION_STORAGE"]
    context.add_init_script("""(storage => {
    
        const entries = JSON.parse(storage)
        for (const [key, value] of Object.entries(entries)) {
          window.sessionStorage.setItem(key, value)
        }
      
    })('""" + session_storage + "')")

    # Now you can access the full content of the page, including any dynamic content loaded by JavaScript
  html = page.content()


  # print(html)

  browser.close()