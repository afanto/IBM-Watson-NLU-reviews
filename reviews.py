from reviews_import import review_text_list, rating_value_list

review_text_positive = []
for index in range(len(rating_value_list)):
   if(rating_value_list[index] == 50 or rating_value_list[index] == 40):
        review_text_positive.append(review_text_list[index])

review_text_negative = []
for index in range(len(rating_value_list)):
    if(rating_value_list[index] == 10 or rating_value_list[index] == 20):
        review_text_negative.append(review_text_list[index])

review_text_positive = [s.rstrip() for s in review_text_positive] #remove newline (/n)
review_text_positive = [item for item in review_text_positive if len(item) > 50] #omit reviews shorter than 50 characters
review_text_negative = [s.rstrip() for s in review_text_negative] #remove newline (/n)
review_text_negative = [item for item in review_text_negative if len(item) > 50] #omit reviews shorter than 50 characters

no_reviews = len(review_text_list)
