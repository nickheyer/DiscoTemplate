from django.urls import re_path

from DiscoTemplateClient.consumers import client

websocket_urlpatterns = [
    re_path(r'ws/client/$', client.ClientConsumer.as_asgi())
]