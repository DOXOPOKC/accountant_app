from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from .models import DocumentsPackage
from .serializers import PackageFullSerializer

class BluebirdConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.package_id = self.scope['url_route']['kwargs']['package_id']
        async_to_sync(self.channel_layer.group_add)(self.package_id,
                                                    self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.package_id,
                                                        self.channel_name)

    def recieve(self, text_data):
        obj = DocumentsPackage.objects.get(id=self.package_id)
        message = PackageFullSerializer(obj)
        async_to_sync(self.channel_layer.group_send)(
            self.package_id,
            {
                'type': 'send_package',
                'message': message.data
            }
        )

    def send_package(self, event):
        message = event['message']
        self.send(message)
