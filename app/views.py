from django.shortcuts import render
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.contrib import messages


class Home(APIView):
  def get(self,request):    
    return render(request, "home.html")

class Login(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self,request):    
    return render(request,"login.html")

  def post(self, request):
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f' wecome {username} !!')
                return HttpResponseRedirect('userprofile')
            else:
              print("inactive")
              return HttpResponse("Inactive user.")
        else:
          print("create a user")
          return HttpResponse('Create a user.')        



class userProfile(APIView):
  def get(self,request):
    return Response("userprofile")