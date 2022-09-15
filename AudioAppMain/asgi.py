"""
ASGI config for AudioAppMain project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from audio_broadcast.consumers import AudioConsumer
import audio_broadcast.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AudioAppMain.settings')
django.setup()

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            audio_broadcast.routing.websocket_urlpatterns
        )
    )
})
