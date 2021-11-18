from django.urls import path
from rooms.views import RoomListView, RoomDetailView

urlpatterns = [
    path('', RoomListView.as_view()),
    path('/<int:room_id>', RoomDetailView.as_view()),
]