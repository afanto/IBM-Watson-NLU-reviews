from ibm_watson import ApiException
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

from reviews import review_text_negative

def _negative(natural_language_understanding):

    no_negative_reviews = len(review_text_negative)
    print("Numer of eligible negative reviews to be processed: " + str(no_negative_reviews))

    health_conditions = []
    processed = no_negative_reviews

    for it in range(len(review_text_negative)):
        try:
            response = natural_language_understanding.analyze(
                text=review_text_negative[it],
                features=Features(entities=EntitiesOptions())).get_result()

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            processed -= 1

        for r in response['entities']:
            if(r['type'] == 'HealthCondition'):
                health_conditions.append(r['text'])

    health_conditions_merged, occurrences = [], []
    [health_conditions_merged.append(x) for x in health_conditions if x not in health_conditions_merged]

    for element in health_conditions_merged:
        occurrences.append(health_conditions.count(element))

    negative = list(zip(health_conditions_merged, occurrences))
    negative.sort(key = lambda x:x[1], reverse=True)

    return negative
