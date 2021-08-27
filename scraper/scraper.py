#imports: BS4, Selenium, Json
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
import json

#Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://username:password@clusterxxx.mongodb.net/database-name?retryWrites=true&w=majority")
db = client.products

#Product ID & number of reviews
product_id = input("Enter product id: ")
product_reviews = input("Enter number of reviews: ")

number_of_pages = 1
if (int(product_reviews) > 999):
    number_of_pages = -(-int(product_reviews) // 1000)

for page in range(number_of_pages):

    #Launching webdriver via Selenium (Chrome)
    driver = webdriver.Chrome()
    driver.get('https://www.iherb.com/ugc/api/review/adaptive?pid='+product_id+'&limit='+product_reviews+'&lc=en-US&page='+str(page)+'&sortId=2&withUgcSummary=true&withImagesOnly=false&isShowTranslated=false')

    #Parsing page source and converting it to json format
    soup = BeautifulSoup(driver.page_source,'html.parser')
    site_json = json.loads(soup.text)

    #Storing review text & ratings in two lists
    review_text = [d.get('reviewText') for d in site_json['items'] if d.get('reviewText')]
    rating_value = [d.get('ratingValue') for d in site_json['items'] if d.get('ratingValue')]

    #Store reviews in MongoDB, two arrays
    record = {'review_text': review_text, 'rating_value': rating_value}
    db.ginko.insert_one(record)

    driver.quit()
