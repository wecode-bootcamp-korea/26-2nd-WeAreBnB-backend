import json, datetime

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Count

from .models import *

class RoomDetailView(View):
    def get(self, request, room_id):
        try:
            room           = Room.objects.get(id = room_id)
            average_rating = room.review_set.aggregate(average = Avg('rating'))['average']

            if average_rating == None:
                average_rating = 0

            result = {
                'room_info' : {
                    'id'                  : room.id,
                    'host'                : room.host_user.name,                    
                    'room_type'           : room.room_type.name,
                    'title'               : room.title,
                    'description'         : room.description,
                    'price'               : round(room.price,0),
                    'max_guest'           : room.max_guest,
                    'bedroom'             : room.bedroom,
                    'bed'                 : room.bed,
                    'bath'                : room.bath,
                    'room_option'         : [{
                        'roomOption_name' : room_option.name,
                        'roomOption_url'  : room_option.image_url
                        } for room_option in room.options.all()],
                    'location'       : room.location.address,
                    'latitude'       : float(room.location.latitude),
                    'longitude'      : float(room.location.longitude),
                    'average_rating' : average_rating,
                    'review_count'   : room.review_set.aggregate(Count('id'))['id__count']
                },
                'reservation_date' : [{
                    'check_in'     : reservation.check_in,
                    'check_out'    : reservation.check_out,
                    'days'         : reservation.days
                } for reservation in room.reservation_set.all()],
                'room_image' : [
                    roomimage.image_url for roomimage in room.room_images.all()
                    ],
                'review_info'      : [{
                    'username'     : review.user.name,
                    'user_profile' : review.user.profile_image_url,
                    'title'        : review.title,
                    'content'      : review.content,
                    'rating'       : review.rating,
                    'date'         : datetime.datetime.strftime(review.created_at, '%Y/%m')
                } for review in room.review_set.all()]
            }
            return JsonResponse({'results' : result}, status = 200)

        except Room.DoesNotExist:
            return JsonResponse({"message" : "방 정보가 없습니다."}, status=404)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)