from ibm_watson import ApiException
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions

from reviews import review_text_positive

def _positive(natural_language_understanding, relevance):

    no_positive_reviews = len(review_text_positive)
    print("Numer of eligible negative reviews to be processed: " + str(no_positive_reviews))

    score, label = [], []
    processed = no_positive_reviews

    for it in range(len(review_text_positive)):
        try:
            response = natural_language_understanding.analyze(
                text=review_text_positive[it],
                features=Features(categories=CategoriesOptions())).get_result()

        except ApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
            processed -= 1

        for r in response['categories']:
            if (int(r['score'] > relevance)):
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

    output = list(zip(label_merged, occurrences, score_avg))
    output.sort(key = lambda x:x[1], reverse=True)

    positive = []
    for index in range(len(output)):
        if (output[index][0][0:7] == "/health" and output[index][1] > 1): positive.append(output[index])

    return positive
