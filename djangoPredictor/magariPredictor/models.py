from django.db import models

# Create your models here.

class Make(models.Model):
    make = models.TextField()

    def __str__ (self):
        return self.make

    class Meta:
        db_table = 'vehicle_make'  

class Model(models.Model):
    model = models.TextField()
    make = models.ForeignKey(Make, on_delete=models.CASCADE)


    def __str__ (self):
        return self.model

    class Meta:
        db_table = 'vehicle_model'

class Vehicle_Images(models.Model):
    make = models.TextField()
    model = models.TextField()
    yom = models.IntegerField()
    mileage = models.IntegerField()
    engine_size = models.IntegerField()
    fuel_type = models.TextField()
    transmission = models.TextField()
    price = models.IntegerField()
    image_url = models.CharField(max_length=255)  # You should specify a max_length for CharField

    def __str__(self):
        return f"Make: {self.make}, Model: {self.model}, Year of Manufacture: {self.yom}, Mileage: {self.mileage}, Engine Size: {self.engine_size}, Fuel Type: {self.fuel_type}, Transmission: {self.transmission}, Price: {self.price}, Image URL: {self.image_url}"
    
    class Meta:
        db_table = 'vehicle_images'

class Vehicle_Data(models.Model):
    make = models.TextField()
    model = models.TextField()
    yom = models.IntegerField()
    mileage = models.IntegerField()
    engine_size = models.IntegerField()
    fuel_type = models.TextField()
    transmission = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return f"Make: {self.make}, Model: {self.model}, Year of Manufacture: {self.yom}, Mileage: {self.mileage}, Engine Size: {self.engine_size}, Fuel Type: {self.fuel_type}, Transmission: {self.transmission}, Price: {self.price}"
    
    class Meta:
        db_table = 'vehicle_data'

