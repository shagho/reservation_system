from django.urls import path
from .views import *


urlpatterns = [
    path('place/<int:id>', place.as_view(), name='place_view'),
    path('', index, name='index'),
]
