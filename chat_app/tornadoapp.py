import tornado


class MessagesHandler(object):
    pass


application = tornado.web.Application([
    (r'/(?P<thread_id>\d+)/', MessagesHandler),
])
