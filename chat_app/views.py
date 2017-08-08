from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

from chat_app.models import Message, Room


class ChatView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat_template.html'
    ordering = '-posted_at'
    context_object_name = 'messages'

    # def dispatch(self, request, *args, **kwargs):
    #     self.kwargs.get('room_slug')

    def get_queryset(self):
        self.qs = super().get_queryset()

        room_slug = self.kwargs.get('room_slug')
        self.qs = self.qs.filter(room__slug = room_slug).select_related('author')

        return self.qs

    def get_context_data(self, **kwargs):
        room_slug = self.kwargs.get('room_slug')

        room = Room.objects.get(slug=room_slug)

        users = Message.objects.filter(room=room)\
            .values('author__username')\
            .annotate(msg_count=Count("id"))\
            .order_by('-msg_count')

        kwargs.update({
            'users': users,
            'room': room,
        })

        return super(ChatView, self).get_context_data(**kwargs)
