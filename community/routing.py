from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/forum/<str:forum_id>/', consumers.ChatConsumer.as_asgi()),
]