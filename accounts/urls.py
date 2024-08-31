from django.urls import path
from accounts import views

urlpatterns = [
    path("login/", views.userLogin.as_view(), name='login'),
    path('login-otp/', views.otpLogin.as_view(), name='login_otp'),
]