from channels.generic.websocket import WebsocketConsumer

class PollsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        "Handle incoming WebSocket data"
        # I hate the dreadful hollow behind the little wood,
        # Its lips in the field above are dabbled with blood-red heath,
        # The red-ribb'd ledges drip with a silent horror of blood,
        # And Echo there, whatever is ask'd her, answers "Death."
        if text_data == "echo":
            self.send(text_data="death")