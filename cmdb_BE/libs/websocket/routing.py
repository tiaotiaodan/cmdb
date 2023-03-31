from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import re_path
from libs.websocket.terminal import SSHConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^server/terminal/(?P<ssh_ip>.*)/(?P<ssh_port>\d+)/(?P<credential_id>\d+)/', SSHConsumer.as_asgi()),  #python 3.6 以上的版本需要“as_asgi()”。
        ])
    ),
})
