from reviews_import import review_text_list, rating_value_list

print("Number of reviews: " + str(len(rating_value_list)))

review_text_list_5 = []

for index in range(len(rating_value_list)):
    if(rating_value_list[index] == 50):
        review_text_list_5.append(review_text_list[index])

print("Numer of 5 start reviews to be processed: " + str(len(review_text_list_5)))

review_text_list_5 = [s.rstrip() for s in review_text_list_5] #remove newline (/n)
review_text_list_5 = [item for item in review_text_list_5 if len(item) > 50] #omit reviews shorter than 50 characters

print("Numer of 5 start reviews to be processed (after cleaning): " + str(len(review_text_list_5)))
