import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import gym_app.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            gym_app.chat.routing.websocket_urlpatterns
        )
    ),
})
