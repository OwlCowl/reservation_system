from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(max_length=255)

class Meta:
    unique_together = ('date', 'room_id',)



