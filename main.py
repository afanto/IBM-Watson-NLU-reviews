from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from reviews import no_reviews
from reviews_positive import _positive
from reviews_negative import _negative

authenticator = IAMAuthenticator('redacted')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-12-02',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('redacted')

print("Total number of reviews: " + str(no_reviews))

print("Watson(positive) - Categories\n")
for element in _positive(natural_language_understanding, 0.65):
    print(element)

print("Watson(negative) - Side effects")
for element in _negative(natural_language_understanding):
    print(element)
