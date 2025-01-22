
class Communicator:
    def __init__(self):
        self.initiator = False

    def send_initiator(self, initiator):
        self.initiator = initiator

    def get_initiator(self):
        return self.initiator
