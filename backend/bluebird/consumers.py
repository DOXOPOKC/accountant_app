from channels.generic.websocket import JsonWebsocketConsumer


class BluebirdConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def recieve(self, text_data):
        print(text_data)
        self.send(text_data)