from django.urls import path
from reviews.views import ReviewsView

urlpatterns = [
    path("/<int:room_id>", ReviewsView.as_view()),
]