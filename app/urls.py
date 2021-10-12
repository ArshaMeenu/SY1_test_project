from django.urls import path
from . import views
urlpatterns = [
  
    path('home',views.Home.as_view(),name = "home"),
    path('login',views.Login.as_view(),name = "login"),
    path('userprofile',views.userProfile.as_view(),name = "userprofile"),
    path('logout',views.Logout.as_view(),name = "logout"),
    path('create_checkout_session/<pk>/',views.CreateCheckoutSessionView.as_view(),name = "create_checkout_session"),
    path('',views.LandingPage.as_view(),name = "langing_page"),
    path('success/',views.SuccessView.as_view(),name = "success_view"),
    path('cancel/',views.CancelView.as_view(),name = "cancel_view"),








]
