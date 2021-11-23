from django.db import models

class Room(models.Model):
    location    = models.ForeignKey('RoomLocation', on_delete=models.CASCADE)
    host_user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    room_type   = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    description = models.TextField()
    price       = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    max_guest   = models.IntegerField(default=0)
    bedroom     = models.IntegerField(default=0)
    bed         = models.IntegerField(default=0)
    bath        = models.IntegerField(default=0)
    created_at  = models.DateField()
    options     = models.ManyToManyField('Option', through='RoomOption')
    
    class Meta:
        db_table = 'rooms'
        
    def __str__(self):
        return self.title
    
class RoomOption(models.Model):
    room   = models.ForeignKey('Room', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'room_options'

class Option(models.Model):
    name      = models.CharField(max_length=100)
    image_url = models.CharField(max_length=1000, null=True)
    
    class Meta:
        db_table = 'options'
        
    def __str__(self):
        return self.name
    
class RoomImage(models.Model):
    room      = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='room_images')
    image_url = models.CharField(max_length=1000, null=True)
    
    class Meta:
        db_table = 'room_images'
        
    # def __str__(self):
    #     return self.room
    
class RoomType(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'room_types'
        
    def __str__(self):
        return self.name
    
class RoomLocation(models.Model):
    country   = models.CharField(max_length=100)
    city      = models.CharField(max_length=100)
    address   = models.CharField(max_length=100)
    latitude  = models.DecimalField(max_digits=16, decimal_places=14, default=0.0)
    longitude = models.DecimalField(max_digits=17, decimal_places=14, default=0.0)
    
    class Meta:
        db_table = 'room_locations'