import signal
import time

import tornado.httpserver
import tornado.ioloop

from django.core.management.base import BaseCommand, CommandError

from chat_app.tornadoapp import application


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            port = int(options.get('port', '8888'))
        except ValueError:
            raise CommandError('Invalid port number specified')

        self.http_server = tornado.httpserver.HTTPServer(application)
        self.http_server.listen(port, address="127.0.0.1")
