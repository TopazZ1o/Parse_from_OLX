import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

link = "https://www.olx.kz/hobbi-otdyh-i-sport/sport-otdyh/astana/?page=1&search%5Border%5D=created_at%3Adesc"

driver = webdriver.Chrome()
chrome_options = Options()
driver.get(link)
test = driver.find_element_by_class_name("form-control")

