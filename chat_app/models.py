from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)

    joined_users = models.ManyToManyField(User,
                                          through='RoomAttendence', through_fields=('room', 'user',),
                                          related_name='rooms', related_query_name='room')


class RoomAttendence(models.Model):
    nickname = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('room', 'nickname'), ('user', 'room'),)


class Message(models.Model):
    text = models.CharField(max_length=512, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    posted_at = models.DateTimeField(auto_now_add=True)
