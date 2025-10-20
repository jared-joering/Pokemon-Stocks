from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager 
from bs4 import BeautifulSoup

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service = service)
destination_folder = "data/log"

# def scrape_pricecharting():
