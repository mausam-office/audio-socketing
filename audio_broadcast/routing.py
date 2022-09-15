from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/test/', consumers.AudioConsumer.as_asgi()),
    re_path(r'ws/test2/', consumers.TempConsumer.as_asgi())
]