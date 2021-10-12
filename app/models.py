from django.db import models

class Events(models.Model):
  event_name = models.CharField(max_length= 100)
  description  = models.TextField(max_length= 255)
  created_at = models.DateTimeField(auto_now=True)
  no_of_members = models.IntegerField()


  def __str__(self):
    return self.event_name
