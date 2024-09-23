from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)

class RefreshToken(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    token = models.CharField(max_length=300)
    user_id = models.IntegerField()