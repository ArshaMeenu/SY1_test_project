from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
import datetime


class Events(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  event_name = models.CharField(max_length= 100, blank=True,null=True)
  description  = models.TextField(max_length= 255,blank=True,null=True)
  start_date = models.DateField(blank=True,null=True)
  end_date = models.DateField(blank=True,null=True)
  is_paid = models.BooleanField(default=False,blank=True,null=True)  
  # country =CountryField(multiple=True,blank=True)
  price= models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
        return self.event_name 

  def get_display_price(self):
    return "{0:.2f}".format(self.price / 100)


class UserProfile(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  full_name = models.CharField(max_length=50)  
  photo_url =models.CharField(max_length=500,blank=True,null=True)
  land_number = models.CharField(max_length=15,blank=True,null=True)
  mobile_number = models.CharField(max_length=15)
  image = models.ImageField(upload_to='images/',null=True, blank=True)

  def __str__(self):
    return self.full_name
