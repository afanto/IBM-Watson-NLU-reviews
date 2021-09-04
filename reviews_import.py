import pymongo

client = pymongo.MongoClient("redacted")
db = client.products

review_text = db.Ashwagandha.find_one({},{"_id":0,"review_text":1})
review_value = db.Ashwagandha.find_one({},{"_id":0,"rating_value":1})

review_text_list, rating_value_list = [], []

for reviews in list(review_text.values()):
    for review in reviews: review_text_list.append(review)

for rates in list(review_value.values()):
    for rate in rates: rating_value_list.append(rate)
