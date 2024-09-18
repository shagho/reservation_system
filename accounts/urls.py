from django.urls import path
from accounts import views

urlpatterns = [
    path("login/", views.otpLogin.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]