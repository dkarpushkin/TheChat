"""Chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from chat_app.views import ChatView, JoinRoomView

urlpatterns = [
    #   редирект на комнату 'mainroom' - она одна единственная
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('room', kwargs={'room_slug': 'mainroom'})),
        name='lobby'),

    url(r'^room/(?P<room_slug>[\w\d\-]+)/$',
        ChatView.as_view(),
        name='room'),
    url(r'^joinroom/(?P<room_slug>[\w\d\-]+)/(?P<nickname>[\w\d-]+)/$',
        JoinRoomView.as_view(),
        name='joinroom')
]
