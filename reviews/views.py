from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count, Avg
from datetime         import datetime

from rooms.models     import Room
from reviews.models   import Review
from core.utils       import login_required

class ReviewsView(View):
    def get(self, request, room_id):
        try:
            room           = Room.objects.get(id = room_id)
            average_rating = room.review_set.aggregate(average = Avg('rating'))['average']

            if not average_rating:
                average_rating = 0

            result = {
                'review_info'      : [{
                        'username'     : review.user.name,
                        'user_profile'  : review.user.profile_image_url,
                        'title'        : review.title,
                        'content'      : review.content,
                        'rating'       : review.rating,
                        'date'         : datetime.strftime(review.created_at, '%Y/%m')
                } for review in room.review_set.all()],
                        'average_rating' : average_rating,
                        'review_count'   : room.review_set.aggregate(Count('id'))['id__count']
            }

            return JsonResponse({'results' : result}, status=200)

        except Room.MultipleObjectsReturned:
            return JsonResponse({'message': 'MULTIPLE_ROOM'}, status = 400)

        except Room.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST_ROOM'}, status = 404)        

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class MyReviewsView(View):
    @login_required
    def get(self, request):
        user = request.user
        
        results = {
            'reviews': [{
                'review_id' : review.id,
                'user_name' : review.user.name,
                'room'      : review.room.title,
                'title'     : review.title,
                'content'   : review.content,
                'created_at': review.created_at
            } for review in Review.objects.filter(user = user)]
        }
        return JsonResponse({'results' : results}, status = 200)
