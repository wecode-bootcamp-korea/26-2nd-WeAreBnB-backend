import json

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q, Count, Avg
from datetime               import datetime, timedelta

from rooms.models           import Room
from reservations.models    import Reservation

class RoomListView(View):
    def get(self, request):
        check_in       = request.GET.get('check_in', None)
        check_out      = request.GET.get('check_out', None)
        offset         = int(request.GET.get('offset', 0))
        limit          = int(request.GET.get('limit', 15))
        ordering       = request.GET.get('sort', 'id')
        reserved_rooms = []
        
        filter_field = {
            'location'    : 'location__address__icontains',  
            'guest'       : 'max_guest__gte',
            'price_max'   : 'price__lte',
            'price_min'   : 'price__gte',
            'room_type'   : 'room_type__name__in',
            'room_option' : 'options__name__in',
        }
        filter_set = {
            filter_field.get(key) : value[0] for (key, value) in dict(request.GET).items() if filter_field.get(key)
        }
        if filter_set.get('options__name__in'):
            filter_set['options__name__in'] = request.GET.getlist('room_option')
        if filter_set.get('room_type__name__in'):
            filter_set['room_type__name__in'] = request.GET.getlist('room_type')
        
        
        if check_in and check_out: 
            check_in_dt  = datetime.strptime(check_in, '%Y-%m-%d')  
            check_out_dt = datetime.strptime(check_out, '%Y-%m-%d') 

            q = Q()
            q |= Q(check_in__range  = [check_in, check_out_dt-timedelta(days=1)])
            q |= Q(check_out__range = [check_in_dt-timedelta(days=-1), check_out])

            reserved_rooms = Reservation.objects.filter(q)

        rooms = Room.objects.filter(**filter_set)\
                            .exclude(reservation__in=reserved_rooms)\
                            .select_related('room_type', 'location')\
                            .prefetch_related('room_images', 'options', 'review_set')\
                            .annotate(review_count=Count('review__id'))\
                            .annotate(review_rating=Avg('review__rating'))\
                            .order_by(ordering)[offset:offset+limit]     
        results = [{
            'room_id'      : room.id,
            'title'        : room.title,
            'price'        : float(room.price),
            'days'         : (check_out_dt - check_in_dt).days if check_in else 0,
            'room_detail'  : { 'max_guest' : room.max_guest,
                                'bedroom'  : room.bedroom,
                                'bed'      : room.bed,
                                'bath'     : room.bath },
            'room_type'    : room.room_type.name,
            'room_options' : [option.name for option in room.options.all()],
            'review'       : room.review_count,
            'rating'       : room.review_rating,
            'latitude'     : float(room.location.latitude),
            'longitude'    : float(room.location.longitude),
            'address'      : room.location.address,
            'images'       : [image.image_url for image in room.room_images.all()],
        } for room in rooms]
        
        return JsonResponse({'results' : results}, status=200)

class RoomDetailView(View):
    def get(self, request, room_id):
        try:
            room           = Room.objects.get(id = room_id)

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
                    'room_image' : [
                        roomimage.image_url for roomimage in room.room_images.all()],
                    'location'       : room.location.address,
                    'latitude'       : float(room.location.latitude),
                    'longitude'      : float(room.location.longitude)
                }
            }
            return JsonResponse({'results' : result}, status = 200)

        except Room.DoesNotExist:
            return JsonResponse({"message" : "INVALID_ROOMS"}, status=404)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

