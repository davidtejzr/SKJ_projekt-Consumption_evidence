from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    motor = models.CharField(max_length=80, null=True)
    fuel = models.CharField(max_length=50)
    fuelTank = models.FloatField()
    kilometresCount = models.FloatField()
    refuelCount = models.IntegerField(default=0)
    longTermConsumption = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(null=True)


class Record(models.Model):
    kilometresCount = models.FloatField()
    fuelType = models.CharField(max_length=20)
    liters = models.FloatField()
    pricePerLiter = models.FloatField()
    price = models.FloatField()
    fullTank = models.BooleanField(default=False)
    fuelTankActualState = models.FloatField()
    shortTermConsumption = models.FloatField(default=0)
    missingRecord = models.BooleanField(default=False)
    refuelDate = models.DateTimeField('refueled', auto_now_add=True)
    tankStation = models.CharField(max_length=255, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
