from django.shortcuts import render
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
          return HttpResponse(f"{username} or password doesn't exit.")
                  

 

class userProfile(APIView):
  def get(self,request, *args, **kwargs):
    return render(request,'userprofile.html')

  def post(self, request, *args, **kwargs):
        serializer_obj = EventSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return render(request,'home.html', status=status.HTTP_201_CREATED)
        return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
  def get(self,request, *args, **kwargs):
    logout(request)
    return render(request,'home.html')