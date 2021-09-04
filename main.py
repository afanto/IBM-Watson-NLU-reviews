from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions

from reviews import review_text_list_5

authenticator = IAMAuthenticator('---')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('---')

score, label = [], []
processed = len(review_text_list_5)
for it in range(len(review_text_list_5)):
    try:
        response = natural_language_understanding.analyze(
            text=review_text_list_5[it],
            features=Features(categories=CategoriesOptions())).get_result()
    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        processed -= 1

    for r in response['categories']:
        if (int(r['score'] > 0.65)): #only include labels with relevance score of >0.65
            score.append((r['score']))
            label.append((r['label']))

print("Successfully processed " + str(processed) + " reviews.")

label_merged, occurrences, score_avg = [], [], []
[label_merged.append(x) for x in label if x not in label_merged]

for element in label_merged:
    occurrences.append(label.count(element))

for index in range(len(label_merged)):
    sum = 0
    for index2 in range(len(label)):
        if (label_merged[index] == label[index2]):
            sum += score[index2]
    score_avg.append(sum/occurrences[index])

_output = list(zip(label_merged, occurrences, score_avg))
_output.sort(key = lambda x:x[1], reverse=True)

_output_cleaned = []
for index in range(len(_output)):
    if (_output[index][0][0:7] == "/health" and _output[index][1] > 1): _output_cleaned.append(_output[index])

for element in _output_cleaned: print(element)
