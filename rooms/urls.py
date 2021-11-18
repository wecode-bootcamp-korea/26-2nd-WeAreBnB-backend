from django.urls import path, include
from .views import RoomDetailView

urlpatterns = [
    path('/<int:room_id>', RoomDetailView.as_view()),
]