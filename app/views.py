from django.shortcuts import render
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class Home(APIView):
  def get(self,request):
    print('abc')
    return render(request, "home.html")

class Login(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self,request):
    print(request.user)
    return render(request,"login.html")


