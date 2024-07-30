"""
ASGI config for FLARE project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing  import ProtocolTypeRouter, URLRouter
import community.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FLARE.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            community.routing.websocket_urlpatterns
        )
    ),
})

app = application