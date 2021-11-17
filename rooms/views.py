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
        ordering       = request.GET.get('sort', 'id')
        reserved_rooms = []
        
        filter_field = {
            'location'    : 'location__address__icontains',  
            'guest'       : 'max_guest__gte',
            'price_max'   : 'price__lte',
            'price_min'   : 'price__gte',
            'room_type'   : 'room_type__name',
            'room_option' : 'options__name__in',
        }
        filter_set = {
            filter_field.get(key) : value[0] for (key, value) in dict(request.GET).items() if filter_field.get(key)
        }
        if filter_set.get('options__name__in'):
            filter_set['options__name__in'] = request.GET.getlist('room_option')
        
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
                            .order_by(ordering)       
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