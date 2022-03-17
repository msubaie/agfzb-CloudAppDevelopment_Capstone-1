from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(max_length=20, default='name')
    description = models.CharField(max_length=200, default='description')

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
