# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:40:45 2022

@author: Vimal Raj
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("C:/Users/Vimal Raj/Documents/chromedriver_win32/chromedriver")

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
driver.get("https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off")

content = driver.page_source
soup = BeautifulSoup(content, features="lxml")

for a in soup.findAll('div', attrs={'class':'_3pLy-c'}):
    name = a.find('div', attrs={'class': '_4rR01T'})
    price = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'})
    rating = a.find('div', attrs={'class': '_3LWZlK'})
    products.append(name.text)
    prices.append(price.text)
    ratings.append(rating.text) 

df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
df.to_csv('products.csv', index=False, encoding='utf-8')