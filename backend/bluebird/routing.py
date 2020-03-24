from django.urls import path

from .consumers import BluebirdConsumer


websocket_urlpatterns = [
    path('ws/contragents/<int:pk>/packages/<int:package_id>/',
         BluebirdConsumer),
]
