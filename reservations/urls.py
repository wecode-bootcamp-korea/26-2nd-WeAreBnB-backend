from django.urls import path
from reservations.views import ReservationsView, ReservationView, ReservationDateView

urlpatterns = [
    path('', ReservationsView.as_view()),
    path('/<str:reservation_code>', ReservationView.as_view()),
    path('/detail/<int:room_id>', ReservationDateView.as_view())
]