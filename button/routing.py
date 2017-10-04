from channels.routing import route

channel_routing = [
    route("http.request", "socket_button.consumers.http_consumer")
]