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
    emp = Events.objects.filter(is_active=1)
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
        email1 = request.POST['username']
        print(email1)
        password = request.POST['password']
        print(password)
        try:
            print(2)
            Account = User.objects.get(username=email1)
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
            print(6)
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["email_address"] = Account.email
                print(7)
                Res = {"data": data, "token": token}
                # return Response(Res)
                msg = "success"
                return render(request, "userprofile.html", { "msg" : msg})


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


  # def post(self, request):
  #       username = request.POST['username']
  #       password = request.POST['password']
  #       print(password)
  #       print(username)

  #       user = authenticate(username=username, password=password)
  #       print(3)
  #       if user is not None:
  #           print(4)
  #           if user.is_active:
  #               print(5)
  #               login(request, user)
  #               context = username
  #               print(context)
  #               return Response('pooi')
  #               # return render(request,'userprofile.html',{'user':context})
                
  #           else:
  #             return HttpResponse("Inactive user.")
  #       else:
  #         # return render(request,'login.html',status=status.HTTP_400_BAD_REQUEST)

  #         return HttpResponse(f"username or password doesn't exit or incorrect.")

class userProfile(APIView):
  def get(self,request, *args, **kwargs):
    return render(request,'userprofile.html')

  def post(self, request, *args, **kwargs):
        serializer_obj = EventSerializer(data=request.data)
        if serializer_obj.is_valid():            
            serializer_obj.save()
            data = serializer_obj.data
            evnt_name = data['event_name']
            price = data['price']
            evnt_id = data['id']            
            return render(request,'checkout.html',{'name':evnt_name,'price':price,'id':evnt_id} ,status=status.HTTP_201_CREATED)
        return render(request,'userprofile.html',status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    return render(request,'home.html')


# stripe section

class CreateCheckoutSessionView(APIView):
  def post(self,request,*args, **kwargs):
    host = self.request.get_host()
    event_id = self.kwargs["pk"]
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








