import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.core.management import call_command
import atexit

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiscoTemplate.settings')
django.setup()

from DiscoTemplateClient.routing import websocket_urlpatterns as client_websocket


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter([
          *client_websocket
        ]))
    ),
})

# AT EXIT CMD
atexit.register(call_command, 'sigint')

# AT STARTUP CMD
call_command('initializedb')
call_command('startloop')

