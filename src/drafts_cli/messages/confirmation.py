from textual.message import Message


# Custom Message class to be used for confirmation
class ConfirmationMessage(Message):
    def __init__(self, action: str, confirmation: bool, data: dict | None = None):
        super().__init__()
        self.action = action
        self.confirmation = confirmation
        self.data = data
