# Реактивный чат на Django Tornado и WebSockets

Django принимает сообщения, отправляет их через PUB/SUB в Торнадо.

Торнадо отправляет все новые сообщения подключенным с WebSockets пользователям.

# Порядок запуска:

1. python manage.py fill_db
2. python manage.py starttornado
3. python manage.py runserver
4. redis-server

# Installation:

1. install and run redis-server
2. run python manage.py fill_db
3. run python manage.py starttornado
4. run django server