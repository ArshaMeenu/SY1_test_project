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
            print(123)
            data = serializer_obj.data
            evnt_name = data['event_name']
            price = data['price']
            evnt_id = data['id']             
            print(evnt_id)           

            return render(request,'checkout.html',{'name':evnt_name,'price':price,'id':evnt_id} ,status=status.HTTP_201_CREATED)
        return HttpResponse('All the fields are required.', status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    return render(request,'home.html')


# stripe section

import stripe
from django.shortcuts import redirect,reverse

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
  def post(self,request,*args, **kwargs):
    print(343)
    host = self.request.get_host()
    print(host)
    event_id = self.kwargs["pk"]
    print(event_id)
    event = Events.objects.get(id = event_id)
    print(909)
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                    {
                        'name': event.event_name,
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': event.price,
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
  emp = Events.objects.all()
  serializer = EventSerializer(emp, many=True) 
  data = serializer.data
  context = { 'payment-status':'success'}
  print(context)
  return render(request,'confirmation.html',context)

def paymentCancel(request):
  context = { 'payment-status':'cancel'}
  return render(request,'confirmation.html',context)








