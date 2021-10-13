from django.db import models

class Events(models.Model):
  event_name = models.CharField(max_length= 100)
  description  = models.TextField(max_length= 255)
  created_at = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=False)
  price = models.IntegerField(default= 0) #cents


  def __str__(self):
    return self.event_name

  def get_display_price(self):
    return "{0:.2f}".format(self.price / 100)