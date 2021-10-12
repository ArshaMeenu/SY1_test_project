from django.shortcuts import render
from django.views.generic.base import TemplateView
import rest_framework
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


class Home(APIView):
  def get(self,request): 
    emp = Events.objects.all()
    serializer = EventSerializer(emp, many=True) 
    context = serializer.data
    return render(request, "home.html",{'data':context})

class Login(APIView):
  permission_classes = (AllowAny,)
  def get(self,request):    
    return render(request,"login.html")

  def post(self, request):
        username = request.POST['username']       
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context = username
                return render(request,'userprofile.html',{'user':context})
            else:
              return HttpResponse("Inactive user.")
        else:
          return HttpResponse(f"{username}  {password} doesn't exit or incorrect.")

class userProfile(APIView):
  def get(self,request, *args, **kwargs):
    return render(request,'userprofile.html')

  def post(self, request, *args, **kwargs):
        serializer_obj = EventSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return render(request,'home.html', status=status.HTTP_201_CREATED)
        return HttpResponse('All the fields are required.', status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    return render(request,'home.html')


# stripe section

import stripe 
from django.conf import settings 
from django.http import JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
  template_name = "success.html"

class CancelView(TemplateView):
  template_name = "cancel.html"

class LandingPage(TemplateView):
  template_name = "landing.html"
  def get_context_data(self, **kwargs):
      event = Events.objects.get(event_name = "Eventz 01")
      context = super(LandingPage, self).get_context_data(**kwargs)
      context.update({
        "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY,
        "event":event,
      })
      return context


class CreateCheckoutSessionView(APIView):
  def post(self,request,*args, **kwargs):
    event_id = self.kwargs["pk"]
    event = Events.objects.get(id = event_id)
    print(event)
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {# TODO: replace this with the `price` of the product you want to sell
                    'proce_data':{

                        'currency':'usd',
                        'unit_amount':event.price,
                        'product_data':{
                          'name':event.event_name,
                        }
                    },                                       
                    'quantity': 1,
                },
            ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
    return JsonResponse({ 'id':checkout_session.id })
