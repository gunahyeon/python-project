from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome('/Users/gnh/Downloads/chromedriver')
driver.implicitly_wait(3)
search_input = 'search/카페'

driver.get(f'https://map.naver.com/{search_input}')

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
notices = soup.find_all("ul")
print(notices)
