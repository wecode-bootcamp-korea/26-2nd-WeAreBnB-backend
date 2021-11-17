from django.urls import path
from rooms.views import RoomListView

app_name = 'rooms'
urlpatterns = [
    path('', RoomListView.as_view()),
]