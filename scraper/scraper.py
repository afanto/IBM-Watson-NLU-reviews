import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
import json

client = pymongo.MongoClient("mongodb+srv://_user:_password@_server/_database?retryWrites=true&w=majority")
db = client.products

product_id = input("Enter product id: ")
product_reviews = input("Enter number of reviews: ")
number_of_pages = -(-int(product_reviews) // 1000) if (int(product_reviews) > 999) else 1
review_text, rating_value = [], []

for page in range(number_of_pages):

    driver = webdriver.Chrome()
    driver.get('https://www.iherb.com/ugc/api/review/adaptive?pid='+product_id+'&limit='+product_reviews+'&lc=en-US&page='+str(page+1)+'&sortId=2&withUgcSummary=true&withImagesOnly=false&isShowTranslated=false')

    site_json = json.loads(BeautifulSoup(driver.page_source,'html.parser').text)
    review_text.append([d.get('reviewText') for d in site_json['items'] if d.get('reviewText')])
    rating_value.append([d.get('ratingValue') for d in site_json['items'] if d.get('ratingValue')])

    driver.quit()

reviews = {'review_text': review_text, 'rating_value': rating_value}
db.ginko.insert_one(reviews)
