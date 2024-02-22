from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen



# ...DO NOT WORK
driver = webdriver.Chrome(options=options)
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
try:
  element = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.ID, 'loadedButton')))
finally:
  print(driver.find_element_by_id('content').text)
driver.close()