from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html', {})


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html', {})


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf()
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    reviews = get_dealer_reviews_from_cf(dealer_id)
    context["dealer_id"] = dealer_id
    context['review_list'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf(dealer_id)
        context['dealer_id'] = dealer_id
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        user = request.user
        if user.is_authenticated:

            review = dict()
            review["id"] = dealer_id
            review["name"] = user.full_name
            review["dealership"] = dealer_id
            review["review"] = request.POST['review']
            review["purchase"] = request.POST['purchase']
            review["purchase_date"] = request.POST['purchase_date']
            review["car_make"] = request.POST['car']
            review["car_model"] = request.POST['car']
            review["car_year"] = request.POST['car']

            json_payload = dict()
            json_payload["review"] = review

            post_request(json_payload, dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            context['dealer_id'] = dealer_id
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/add_review.html', context)