from django.http import JsonResponse

from django.views import View

from core.utils import login_required
from reservations.models import Reservation
from users.models import User

class ReservationsView(View):
    @login_required
    def get(self, request):
        try:
            user = request.user
            
            results = {
                'reservations': [{
                    'reservation_id': reservation.id,
                    'address'       : reservation.room.location.address,
                    'title'         : reservation.room.title,
                    'image_url'     : reservation.room.room_images.first().image_url,
                    'check_in'      : reservation.check_in,
                    'check_out'     : reservation.check_out
                } for reservation in Reservation.objects.filter(user = user)],
            }

            return JsonResponse({'results' : results}, status = 200)
        
        except Reservation.DoesNotExist:
            return JsonResponse({"message" : "INVALID_RESERVATION"}, status=404)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    def post(self, request):
        pass
        #화연