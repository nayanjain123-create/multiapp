from django.urls import re_path
from .consumers import ChatConsumer, ProductChatConsumer

websocket_urlpatterns = [

    re_path(
        r"ws/chat/(?P<room_id>\w+)/$",
        ChatConsumer.as_asgi()
    ),

    re_path(
        r"ws/product_chat/(?P<room_id>\w+)/$",
        ProductChatConsumer.as_asgi()
    ),
]