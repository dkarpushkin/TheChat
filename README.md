# Реактивный чат на Django Tornado и WebSockets

Django принимает сообщения, отправляет их через PUB/SUB в Торнадо.

Торнадо отправляет все новые сообщения подключенным с WebSockets пользователям.

# Порядок запуска:

1. python manage.py fill_db
2. python manage.py starttornado
3. python manage.py runserver
4. redis-server

# Installation:

vagrant up

In vagrant:

		cd /project
		python3 manage.py migrate
		python3 manage.py fill_db
		python3 manage.py starttornado&
		python3 manage.py runserver 0.0.0.0:8080