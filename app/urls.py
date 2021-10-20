from django.urls import path
from . import views

urlpatterns = [
  
    path('',views.Home.as_view(),name = "home"),
    path('login/',views.Login.as_view(),name = "login"),
    path('userprofile',views.userProfile.as_view(),name = "userprofile"),
    path('payment-confirm',views.paymentConfirm.as_view(),name = "payment-confirm"),
    path('logout',views.Logout.as_view(),name = "logout"),

    # stripe section
    path('create-checkout-session/<pk>/',views.CreateCheckoutSessionView.as_view(),name = "create-checkout-session"),
    path('payment-success/',views.paymentSuccess,name = "payment-success"),
    path('payment-cancel/',views.paymentCancel,name = "payment-cancel"),









]
