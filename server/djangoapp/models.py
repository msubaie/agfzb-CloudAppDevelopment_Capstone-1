from django.db import models
from django.utils.timezone import now


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=20, default='name')
    description = models.CharField(max_length=200, default='description')

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='name')
    dealer_id = models.CharField(max_length=50, default='dealer')
    type = models.CharField(max_length=20, default='type')
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Dealer: " + self.dealer_id + "," + \
               "Type: " + self.type


# Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, id, short_name, full_name, address, city, state, st, zip, lat, long):
        self.id = id
        self.short_name = short_name
        self.full_name = full_name
        self.address = address
        self.city = city
        self.state = state
        self.st = st
        self.zip = zip
        self.lat = lat
        self.long = long

    def __str__(self):
        return "Dealer Name: " + self.full_name


# Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment=0):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Review: " + self.review