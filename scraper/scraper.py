#imports: BS4, Selenium, Json
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
import json

#Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://username:password@clusterxxx.mongodb.net/database-name?retryWrites=true&w=majority")
db = client.products

#Product ID & number of reviews
product_id = input("Enter product id: ") #67652
product_reviews = input("Enter number of reviews: ") #740

#Launching webdriver via Selenium (Chrome)
driver = webdriver.Chrome()
driver.get('https://www.iherb.com/ugc/api/review/adaptive?pid='+product_id+'&limit='+product_reviews+'&lc=en-US&page=1&sortId=2&withUgcSummary=true&withImagesOnly=false&isShowTranslated=false')

#Parsing page source and converting it to json format
page_source = driver.page_source
soup = BeautifulSoup(page_source,'html.parser')
site_json = json.loads(soup.text)

#Storing review text & ratings in two lists
review_text = [d.get('reviewText') for d in site_json['items'] if d.get('reviewText')]
rating_value = [d.get('ratingValue') for d in site_json['items'] if d.get('ratingValue')]

#Store reviews in MongoDB, two arrays
record = {'review_text': review_text, 'rating_value': rating_value}
db.theanine.insert_one(record)
