from django.db      import models
from core.models    import TimeStampModel

class Reservation(TimeStampModel):
    reservation_code = models.CharField(max_length=200)
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room             = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    check_in         = models.DateField()
    check_out        = models.DateField()
    days             = models.IntegerField(default=0)
    adult            = models.IntegerField(default=0)
    children         = models.IntegerField(default=0)
    deleted_at       = models.DateTimeField(null=True)

    class Meta:
        db_table = 'reservations'