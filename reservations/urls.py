from django.urls import path
from reservations.views import ReservationView, ReservationFixView

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/<str:reservation_code>', ReservationFixView.as_view()),
]