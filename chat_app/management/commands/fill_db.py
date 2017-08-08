from django.contrib.auth.models import User
from django.core.management import BaseCommand

from chat_app.models import Room, Message


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fill_test_users()
        self.fill_rooms()
        self.fill_test_messages()

    def fill_test_users(self):
        User.objects.all().delete()
        self.users = []
        self.users.append(User.objects.create_user(username='test_user1', password='default_password'))
        self.users.append(User.objects.create_user(username='test_user2', password='default_password'))
        self.users.append(User.objects.create_user(username='test_user3', password='default_password'))
        self.users.append(User.objects.create_user(username='test_user4', password='default_password'))
        self.users.append(User.objects.create_user(username='test_user5', password='default_password'))
        User.objects.create_user(username='test_user0', password='default_password')

    def fill_rooms(self):
        Room.objects.all().delete()
        self.room = Room.objects.create(name='main room', slug='mainroom')

    def fill_test_messages(self):
        Message.objects.all().delete()
        for user in self.users[::2]:
            Message.objects.create(text='message1', author=user, room=self.room)
            Message.objects.create(text='message2', author=user, room=self.room)
        for user in self.users[1::2]:
            Message.objects.create(text='message1', author=user, room=self.room)
            Message.objects.create(text='message2', author=user, room=self.room)
            Message.objects.create(text='message3', author=user, room=self.room)
