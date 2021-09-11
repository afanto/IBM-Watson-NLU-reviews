from ibm_watson import ApiException
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
import pandas as pd
import json

from reviews import review_text_negative

def _negative(natural_language_understanding):

    no_negative_reviews = len(review_text_negative)
    print("Numer of eligible negative reviews to be processed: " + str(no_negative_reviews))

    health_conditions = []
    processed = no_negative_reviews

    cols = ['review', 'text', 'relevance', 'emotion', 'confidence']
    negative_df = pd.DataFrame(columns=cols)

    for it in range(len(review_text_negative)):
        try:
            response = natural_language_understanding.analyze(
                text=review_text_negative[it],
                features=Features(entities=EntitiesOptions(emotion=True))).get_result()

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            processed -= 1


        l = list()
        for r in response['entities']:
            r_copy = r
            if(r['type'] == 'HealthCondition'):
                health_conditions.append(r['text'])
                r_copy["review"] = review_text_negative[it]
                l.append(r_copy)

        negative_df = negative_df.append(pd.DataFrame(data=l))

    print("Successfully processed " + str(processed) + " reviews.\n")

    negative_df = negative_df.drop(columns='disambiguation')
    negative_df = negative_df.drop(columns='type')

    json_struct = json.loads(negative_df.to_json(orient="records"))
    negative_df = pd.json_normalize(json_struct)

    negative_df.to_csv("Ginkgo_negative.csv", sep='\t')

    health_conditions_merged, occurrences = [], []
    [health_conditions_merged.append(x) for x in health_conditions if x not in health_conditions_merged]

    for element in health_conditions_merged:
        occurrences.append(health_conditions.count(element))

    negative_ = list(zip(health_conditions_merged, occurrences))
    negative_.sort(key = lambda x:x[1], reverse=True)

    negative = []
    for index in range(len(negative)):
        if (negative_[index][1] > 1): negative.append(negative_[index])

    return negative_
