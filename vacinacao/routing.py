from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import agendamento.routing
from django.core.asgi import get_asgi_application
import os 

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             agendamento.routing.websocket_urlpatterns
#         )
#     ),
#     "http": get_asgi_application(),
# })

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacinacao.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
})