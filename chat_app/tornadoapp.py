import tornado
import tornado.gen
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient

import redis
import tornadoredis
import datetime
import importlib

from django.conf import settings

from chat_app.models import User, Room
from chat_app.utils import room_channel_name

session_engine = importlib.import_module(settings.SESSION_ENGINE)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')


class MessagesHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

    def open(self, room_slug, *args, **kwargs):
        try:
            room = Room.objects.get(slug=room_slug)
        except:
            pass
        else:
            self.client.subscribe(room_channel_name(room), self.on_subscribed)

    def on_subscribed(self, *args, **kwargs):
        self.client.listen(self.on_message)

    def on_message(self, message):
        if message.kind == 'message':
            self.write_message(str(message.body))

    def on_close(self):
        try:
            self.client.unsubscribe(self.chanell)
        except AttributeError:
            pass

        def check():
            if self.client.connection.in_progress:
                tornado.ioloop.IOLoop.instance().add_timeout(
                    datetime.timedelta(0.00001),
                    check
                )
            else:
                self.client.disconnect()

        tornado.ioloop.IOLoop.instance().add_timeout(
            datetime.timedelta(0.00001),
            check
        )

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/(?P<room_slug>[\w\d\-]+)/$', MessagesHandler),
])
