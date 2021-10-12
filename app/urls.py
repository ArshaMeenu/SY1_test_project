from django.urls import path
from . import views
urlpatterns = [
  
    path('home',views.Home.as_view(),name = "home"),
    path('login',views.Login.as_view(),name = "login"),
    path('userprofile',views.userProfile.as_view(),name = "userprofile"),
    path('logout',views.Logout.as_view(),name = "logout"),
    # path('addevent',views.addEvent.as_view(),name = "add_event"),





]
