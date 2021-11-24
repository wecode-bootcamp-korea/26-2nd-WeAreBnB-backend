import re
import jwt
import json
import bcrypt
import requests

from datetime        import datetime, timedelta
from django.http     import JsonResponse
from django.views    import View

from config.settings     import SECRET_KEY, ALGORITHM
from users.models        import User
from reservations.models import Reservation
from rooms.models        import Room
from reviews.models      import Review
from core.utils          import login_required

class ReviewsView(View):
    @login_required
    def get(self, request):
        try:
            user    = request.user
            results = {
                'reviews': [{
                    'review_id' : review.id,
                    'user_name' : review.user.name,
                    'room'      : review.room.title,
                    'title'     : review.title,
                    'content'   : review.content,
                    'created_at': review.created_at
                } for review in Review.objects.filter(user = user)],
                
                'room_title_list' : [
                    reservation.room.title for reservation in Reservation.objects
                                                                         .filter(user = user)
                                                                         .select_related('room')
                ]
             }

            return JsonResponse({'results' : results}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    def post(self, request):
        pass