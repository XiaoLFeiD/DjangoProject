from django.urls import path, re_path

from web import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conv_id>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]