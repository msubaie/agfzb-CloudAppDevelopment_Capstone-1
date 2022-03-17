import os
import requests
import json
from .nlu import get_sentiment
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(json_payload, **kwargs):
    try:
        url = "https://35ff1eaf.us-south.apigw.appdomain.cloud/api/review"
        response = requests.post(url, params=kwargs, json=json_payload, headers={'Content-Type': 'application/json'})
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Get dealers from a cloud function
def get_dealers_from_cf():
    results = []
    url = "https://35ff1eaf.us-south.apigw.appdomain.cloud/api/dealership"
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            doc = dealer["doc"]
            dealer = CarDealer(id=doc["id"], short_name=doc["short_name"], full_name=doc["full_name"],
                               address=doc["address"], city=doc["city"], state=doc["state"], 
                               st=doc["st"], zip=doc["zip"], lat=doc["lat"], long=doc["long"])
            results.append(dealer)

    return results


# Quick hack to get single dealer
def get_dealer(url, dealerId):
    result = None
    dealers = get_dealers_from_cf(url)
    for dealer in dealers:
        if dealer["id"] == dealerId:
            result = dealer
            break
    return result


# Get dealer reviews from cloud function
def get_dealer_reviews_from_cf(dealer_id):
    results = []
    url = "https://35ff1eaf.us-south.apigw.appdomain.cloud/api/review?dealership=" + str(dealer_id)
    json_result = get_request(url)
    if json_result:
        reviews = json_result["result"]["docs"]
        for rev in reviews:
            review_obj = DealerReview(id=rev["id"], name=rev["name"], dealership=rev["dealership"],
                               review=rev["review"], purchase=rev["purchase"], purchase_date=rev["purchase_date"], 
                               car_make=rev["car_make"], car_model=rev["car_model"], car_year=rev["car_year"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# This function calls the get_sentiment() function in nlu.py.
def analyze_review_sentiments(text):
    return get_sentiment(text)