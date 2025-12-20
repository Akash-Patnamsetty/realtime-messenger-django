# projectroot/asgi.py
'''''
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import newapp.routing
#from newapp.routing import websocket_urlpatterns 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                newapp.routing.websocket_urlpatterns
            )
        )
    ),
})'''
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newproject.settings")

# ✅ Initialize Django FIRST
django_asgi_app = get_asgi_application()

# ✅ Import routing ONLY AFTER Django setup
import newapp.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                newapp.routing.websocket_urlpatterns
            )
        )
    ),
})

