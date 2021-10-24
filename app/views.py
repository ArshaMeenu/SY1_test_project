import re
from django.shortcuts import render
from django.views.generic.base import TemplateView
import rest_framework
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.contrib import messages
from events.serializers import *
from rest_framework import status
from .models import *
from django.views.generic.list import ListView

import json
from django.contrib.auth.models import User
from rest_framework.exceptions import  ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.core.paginator import  Paginator



# stripe section
import stripe
from django.shortcuts import redirect,reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

# home page section
class Home(ListView):
  permission_classes = (AllowAny,)
  def get(self,request):    
    event_list = Events.objects.filter(is_paid=1).all().values().order_by('start_date')
    paginator = Paginator(event_list, 3) # Show 3 events per page.
    page_number = request.GET.get('page')
    event_obj = paginator.get_page(page_number)        
    return render(request, "home.html",{'data':event_obj})

  def post(self,request):
    event_list = Events.objects.filter(is_paid=1).all().values()
    paginator = Paginator(event_list, 4) # Show 3 events per page.
    page_number = request.GET.get('page')
    event_obj = paginator.get_page(page_number)
    return render(request, "home.html",{'data':event_obj})


# login page section
class Login(APIView):
  permission_classes = (AllowAny,)
  def get(self,request):   
    user = request.user 
    return render(request,"login.html",{'user':user})

  def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        msg ="Invalid username or password."        

        try:          
            Account = User.objects.get(username=username)
        except BaseException as e:
            return render(request, "login.html", { "message" : msg})
        token = Token.objects.get_or_create(user=Account)[0].key
        if not check_password(password, Account.password):
            return render(request, "login.html", { "message" : msg})
        if Account:           
            if Account.is_active:                
                login(request, Account)   
                userid = request.user.id                  
                user = UserProfile.objects.filter(user_id = userid).all()                
                serialized = UserProfileSerializer(user,many=True)
                data=serialized.data
                fullname = data[0].get('full_name')
                username= data[0].get('user')
                request.session['fullname'] = fullname
                request.session['username'] = username
                response = redirect('/userprofile')
                return response
            else:
                return render(request, "login.html", { "message" : msg})
        else:
            return render(request, "login.html", { "msg" : msg})

# user profile section
class userProfile(APIView):
  permission_classes = (AllowAny,)
  def get(self,request, *args, **kwargs):     
    return render(request,'userprofile.html')

  def post(self, request, *args, **kwargs):
    if request.method == "POST":
      event_name = request.POST["event_name"]
      desc = request.POST["description"]
      amount = request.POST["price"] 
      country = request.POST["country"]    
      user = request.session["username"]
      if event_name ==" " or amount ==" " or desc==" " :
        messages.warning(request,"There is one or more fields are empty!")
        return redirect("/userprofile")
      userid = User.objects.filter(username = user).values('id')
      serializer_obj = EventSerializer(data = request.data)  
      if serializer_obj.is_valid():            
          serializer_obj.save(country=country,user_id = userid )
          data = serializer_obj.data 
          evnt_name = data['event_name']
          evnt_id = data['id']  
          payment_status = data['is_paid']
          request.session['event_name']=evnt_name
          request.session['status']=payment_status
          request.session['id']=evnt_id
          return redirect("/payment-confirm")     
      return render(request,'userprofile.html',status=status.HTTP_400_BAD_REQUEST)       
        

# payment confirm page section
class paymentConfirm(APIView):
  def get(self,request, *args, **kwargs):
    id =request.session['id']
    return render(request,'paymentconfirm.html',{'id':id})

# logout section
class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    response = redirect('/login')
    return response

# payment using stripe section

class CreateCheckoutSessionView(APIView):
  def post(self,request,*args, **kwargs):   
    host = self.request.get_host()    
    event_id = self.kwargs["pk"]
    event = Events.objects.get(id=event_id) 
    event.is_paid = 1
    event.save()  
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                    {
                        'name': event.event_name,
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': 10000,
                    }
                ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url = "http://{}{}".format(host,reverse('payment-success')),
            cancel_url = "http://{}{}".format(host,reverse('payment-cancel')),
        )     
    return redirect(checkout_session.url,code=303)

def paymentSuccess(request):  
  msg = "Payment Successfully " 
  return render(request,'success.html',{'message':msg})


def paymentCancel(request):
  context = { 'payment-status':'Payment failed.Please try again later'}
  return render(request,'cancel.html',context)



