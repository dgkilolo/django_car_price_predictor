from django.db import models

# Create your models here.

class Car(models.Model):
    Make = models.IntegerField()
    Model = models.IntegerField()
    Mileage = models.IntegerField()
    Engine_Size = models.IntegerField()
    Fuel_Type = models.IntegerField()
    Transmission = models.IntegerField()
    Age = models.IntegerField()
