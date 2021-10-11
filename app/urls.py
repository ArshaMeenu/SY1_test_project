from django.urls import path
from . import views
urlpatterns = [
  
    path('home',views.Home.as_view(),name = "home"),
    path('login',views.Login.as_view(),name = "login"),
    path('userprofile',views.userProfile.as_view(),name = "userprofile"),



]
