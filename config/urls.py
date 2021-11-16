from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('rooms', include('rooms.urls')),
    path('reservations', include('reservations.urls')),
    path('reviews', include('reviews.urls'))
]
