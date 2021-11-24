import json, uuid

from core.utils              import login_required
from django.views            import View
from django.http             import JsonResponse
from reservations.models     import Reservation
from datetime                import datetime
from rooms.models            import Room
from users.models            import User

class ReservationsView(View):
    @login_required
    def get(self, request):
        pass
        #민정
    
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

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Room.DoesNotExist:
            pass

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
            reservation.adult     = adult
            reservation.children  = children
            reservation.save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except Reservation.MultipleObjectsReturned:
            return JsonResponse({'message': 'MULTIPLE_RESERVATION'}, status = 400)

        except Reservation.DoesNotExist:
            return JsonResponse({'message': 'DOES_NOT_EXIST_RESERVATION'}, status = 400)

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
            return JsonResponse({'message': 'DOES_NOT_EXIST_RESERVATION'}, status = 400)