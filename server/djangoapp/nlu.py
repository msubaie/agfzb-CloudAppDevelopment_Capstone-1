import os
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from dotenv import load_dotenv

load_dotenv()

apikey = os.environ['nlu_apikey']
url = os.environ['nlu_url']

authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(url)


# return sentiment label such as Positive or Negative
def get_sentiment(text):
    """Find sentiment for the given text"""
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())).get_result()
    sentiment = response['sentiment']['document']['label']
    return sentiment