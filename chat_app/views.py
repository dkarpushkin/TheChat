from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.utils import dateformat
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from Chat.utils import JSONResponseMixin
from chat_app.models import Message, Room, RoomAttendence
from chat_app.utils import send_message, room_channel_name


class JoinRoomView(JSONResponseMixin, LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JoinRoomView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        errors = []
        room_slug = self.kwargs.get('room_slug')
        room = Room.objects.get(slug=room_slug)

        user = request.user
        nickname = self.kwargs.get('nickname')

        try:
            RoomAttendence.objects.create(user=user, room=room, nickname=nickname)
        except IntegrityError:
            errors.append('User already joined the channel')

        send_message({
            'type': 'user joined',
            'nickname': nickname,
        }, room_channel_name(room))

        is_ok = (len(errors) == 0)

        return self.render_to_json_response({
            'success': is_ok,
            'errors': errors,
        }, status = 200 if is_ok else 400)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ChatView(JSONResponseMixin, LoginRequiredMixin, ListView):
    """
        Вьюшка для отображения страницы чата (GET запрос)
        и приема сообщений (POST запрос)
    """

    model = Message
    template_name = 'chat_template.html'
    ordering = '-posted_at'
    context_object_name = 'messages'

    def get_queryset(self):
        """ Фильтр сообщений по комнате """

        self.qs = super().get_queryset()

        room_slug = self.kwargs.get('room_slug')
        room = Room.objects.get(slug=room_slug)
        self.qs = self.qs.filter(room__slug = room_slug).select_related('author')

        return self.qs

    def get_context_data(self, **kwargs):
        room_slug = self.kwargs.get('room_slug')

        room = Room.objects.get(slug=room_slug)

        users = room.roomattendence_set.all()
        room_att = room.roomattendence_set.filter(user=self.request.user, room=room)

        kwargs.update({
            'user_atts': users,
            'room': room,
            'user_att': room_att,
            'is_joined': len(room_att) > 0,
        })

        return super(ChatView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
            Прием сообщений

            room_slug - id комнаты
            :return:
            json object: {success: boolean, errors: []}
        """
        room_slug = self.kwargs.get('room_slug')

        errors = []

        try:
            room = Room.objects.get(slug=room_slug)
        except:
            errors.append('Room does not exist')
        else:
            user = request.user
            msg = request.POST.get('text')
            attendance = RoomAttendence.objects.filter(user=user, room=room)

            if not user or not user.is_authenticated:
                errors.append('Not authenticated')
            elif len(attendance) == 0:
                errors.append('User not in this room')
            elif msg is None or len(msg) == 0:
                errors.append('Message is empty')
            else:
                message = Message.objects.create(text=msg, author=user, room=room)
                send_message({
                    'type': 'message sent',
                    'time': dateformat.format(message.posted_at, 'U'),
                    'nickname': attendance.first().nickname,
                    'text': message.text,
                }, room_channel_name(message.room))

        is_ok = len(errors) == 0

        return self.render_to_json_response({
            'success': is_ok,
            'errors': errors,
        }, status = 200 if is_ok else 400)

