import json, uuid

from datetime            import datetime
from django.views        import View
from django.http         import JsonResponse

from core.utils          import login_required
from reservations.models import Reservation
from rooms.models        import Room

class ReservationsView(View):
    @login_required
    def post(self, request):
        try:
            data      = json.loads(request.body)
            room      = data['room']
            check_in  = datetime.strptime(data['check_in'], '%Y-%m-%d')
            check_out = datetime.strptime(data['check_out'], '%Y-%m-%d')
            adult     = data['adult']
            children  = data['children']

            if check_in <= datetime.now():
                return JsonResponse({'message': 'INVALID_DATE'}, status=400)

            if check_in >= check_out:
                return JsonResponse({'message': 'INVALID_DATE'}, status=400)

            if adult + children > Room.objects.get(id=room).max_guest:
                return JsonResponse({'message': 'EXCEED THE QUANTITY'}, status=400)

            reservation = Reservation.objects.create(
                            reservation_code = str(uuid.uuid4()),
                            user_id          = request.user.id,
                            room_id          = room,
                            check_in         = check_in,
                            check_out        = check_out,  
                            days             = (check_out - check_in).days,
                            adult            = adult,
                            children         = children
            )
            return JsonResponse({'reservation_code': reservation.reservation_code}, status = 200)

        except Room.MultipleObjectsReturned:
            return JsonResponse({'message': 'MULTIPLE_ROOM'}, status = 400)

        except Room.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST_ROOM'}, status = 404)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class ReservationView(View):
    @login_required
    def patch(self, request, reservation_code):
        try:
            data        = json.loads(request.body)
            user        = request.user
            adult       = data['adult']
            children    = data['children']
            check_in    = datetime.strptime(data['check_in'], '%Y-%m-%d')
            check_out   = datetime.strptime(data['check_out'], '%Y-%m-%d')
            reservation = Reservation.objects.get(user = user, reservation_code = reservation_code)

            if adult + children > reservation.room.max_guest:
                return JsonResponse({'message': 'EXCEED THE QUANTITY'}, status=400)

            reservation.check_in  = check_in
            reservation.check_out = check_out
            reservation.days      = (check_out - check_in).days
            reservation.adult     = data['adult']
            reservation.children  = data['children']
            reservation.save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except Reservation.MultipleObjectsReturned:
            return JsonResponse({'message': 'MULTIPLE_RESERVATION'}, status = 400)

        except Reservation.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST_RESERVATION'}, status = 404)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @login_required
    def delete(self, request, reservation_code):
        try:
            user        = request.user
            reservation = Reservation.objects.get(user = user, reservation_code = reservation_code)

            reservation.delete()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except Reservation.MultipleObjectsReturned:
            return JsonResponse({'message': 'MULTIPLE_RESERVATION'}, status = 400)

        except Reservation.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST_RESERVATION'}, status = 404)

class ReservationDateView(View):
    def get(self, request, room_id):
        try:
            result = {
                'reservation_date' : [{
                    'check_in'     : reservation.check_in,
                    'check_out'    : reservation.check_out,
                    'days'         : reservation.days
                } for reservation in Reservation.objects.filter(room_id = room_id)]
            }

            return JsonResponse({'results' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class ReservationsView(View):
    @login_required
    def get(self, request):
        user = request.user
        
        results = {
            'reservations': [{
                'reservation_id': reservation.id,
                'address'       : reservation.room.location.address,
                'title'         : reservation.room.title,
                'image_url'     : reservation.room.room_images.first().image_url,
                'check_in'      : reservation.check_in,
                'check_out'     : reservation.check_out
            } for reservation in Reservation.objects.filter(user = user)]
        }

        return JsonResponse({'results' : results}, status = 200)