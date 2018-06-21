# Реактивный чат на Django Tornado и WebSockets

Django принимает сообщения, отправляет их через PUB/SUB в Торнадо.

Торнадо отправляет все новые сообщения подключенным с WebSockets пользователям.


# Installation:

vagrant up

vagrant credentials: vagrant:vagrant

In vagrant:

    cd /project
    python3 manage.py migrate
    python3 manage.py fill_db
    python3 manage.py starttornado
    python3 manage.py runserver