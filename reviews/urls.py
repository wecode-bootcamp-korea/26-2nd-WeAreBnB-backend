from django.urls   import path

from reviews.views import ReviewsView, MyReviewsView

urlpatterns = [
    path('', MyReviewsView.as_view()),
    path("/<int:room_id>", ReviewsView.as_view())
]