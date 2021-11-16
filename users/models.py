from django.db      import models
from core.models    import TimeStampModel

class User(TimeStampModel):
    email             = models.EmailField(max_length=45, unique=True)
    password          = models.CharField(max_length=200)
    name              = models.CharField(max_length=45)
    phone             = models.CharField(max_length=17, null=True)
    profile_image_url = models.CharField(max_length=1000, null=True)
    social_id         = models.CharField(max_length=2000, null=True)
    social_type       = models.CharField(max_length=100, null=True)
    deleted_at        = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.name