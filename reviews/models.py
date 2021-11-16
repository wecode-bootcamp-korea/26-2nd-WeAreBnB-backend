from django.db      import models
from core.models    import TimeStampModel

class Review(TimeStampModel):
    room       = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title      = models.CharField(max_length=100)
    content    = models.TextField()
    rating     = models.FloatField(default=0)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review    = models.ForeignKey('Review', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=1000, null=True)
    
    class Meta:
        db_table = 'review_images'    