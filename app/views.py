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

# stripe section
import stripe
from django.shortcuts import redirect,reverse

stripe.api_key = settings.STRIPE_SECRET_KEY



class Home(APIView):
  def get(self,request): 
    emp = Events.objects.filter(is_paid=0)
    serializer = EventSerializer(emp, many=True) 
    context = serializer.data    
    return render(request, "home.html",{'data':context})

  def post(self,request):
    emp = Events.objects.filter(is_active=1)
    serializer = EventSerializer(emp, many=True) 
    context = serializer.data
    return render(request, "home.html",{'data':context})


import json
from django.contrib.auth.models import User
from rest_framework.exceptions import  ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password


class Login(APIView):
  permission_classes = (AllowAny,)
  def get(self,request):   
    user = request.user 
    return render(request,"login.html",{'user':user})

  def post(self,request):

        data = {}
        reqBody = request.body
        print(1)
        print(reqBody)
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        try:
            print(2)
            Account = User.objects.get(username=username)
            print(Account)
        except BaseException as e:
            print(3)
            msg = str(e)
            return render(request, "login.html", { "msg" : msg})
            # raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=Account)[0].key
        print(4)
        print(token)
        if not check_password(password, Account.password):
            print(5)
            msg ="Incorrect Login credentials"
            return render(request, "login.html", { "msg" : msg})

            # raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
           
            if Account.is_active:                
                login(request, Account)   
                userid = request.user.id                             
                request.session['username'] = username
                request.session['fullname'] = password             
                             
                # return render(request, "userprofile.html", { "msg" : msg})
                response = redirect('/userprofile')
                return response
                # return HttpResponseRedirect(reverse('/userprofile', args=(username, )))

            else:
                print(8)
                # raise ValidationError({"400": f'Account not active'})
                msg = {"400": f'Account not active'}
                return render(request, "login.html", { "msg" : msg})


        else:
            print(9)
            msg= "Account doesnt exist"
            return render(request, "login.html", { "msg" : msg})

            # raise ValidationError({"400": f'Account doesnt exist'})


class userProfile(APIView):
  def get(self,request, *args, **kwargs):
    return render(request,'userprofile.html')

  def post(self, request, *args, **kwargs):
        print(request.data)
        serializer_obj = EventSerializer(data=request.data)        
        if serializer_obj.is_valid():            
            serializer_obj.save()
            print(serializer_obj.data)
            data = serializer_obj.data
            evnt_name = data['event_name']
            start_date = data['start_date']  
            amount = data['price']
            return redirect("/paymentconfirm")     
            # return render(request,'paymentconfirm.html',status=status.HTTP_201_CREATED)
                                       
            # return render(request,'checkout.html',{'name':evnt_name,'start_date':start_date,'amount':amount} ,status=status.HTTP_201_CREATED)
        return render(request,'userprofile.html',status=status.HTTP_400_BAD_REQUEST)


class paymentConfirm(APIView):
  def get(self,request, *args, **kwargs):
    return render(request,'paymentconfirm.html')

class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    # return render(request,'login.html')
    response = redirect('/login')
    return response

# stripe section

class CreateCheckoutSessionView(APIView):
  def post(self,request,*args, **kwargs):
    host = self.request.get_host()
    event_id = self.kwargs["pk"]
    # serializer_obj = EventSerializer(data=request.data)        
    # if serializer_obj.is_valid():
    #   serializer_obj.save()
    event = Events.objects.get(id=event_id) 
    event.is_active = 1
    event.save()  

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
  return render(request,'success.html')

def paymentCancel(request):
  context = { 'payment-status':'cancel'}
  return render(request,'cancel.html',context)





