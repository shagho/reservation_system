from django.urls import path
from .views import *


urlpatterns = [
    path('place/<int:id>', place.as_view(), name='place_view'),
    path('dashboard/reservation_request/<int:id>', AcceptReservation.as_view(), name='accept_reservation'),
    path('dashboard/my_reservation/<int:id>', MyReservation.as_view(), name='my_reservation_delete'),
    path('dashboard/my_reservation', MyReservation.as_view(), name='my_reservation'),
    path('dashboard', Profile.as_view(), name='profile'),
    path('', index, name='index'),
]
