from django import forms
from .models import *


class LoginForm(forms.Form):
  username = forms.CharField(max_length= 63)
  password = forms.CharField(max_length= 50,widget= forms.PasswordInput)


