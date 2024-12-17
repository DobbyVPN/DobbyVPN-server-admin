# ui/message_view.py

from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical



class MessageView(Screen):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.title_text = title
        self.message = message

    def compose(self):
        yield Static(self.title_text)
        yield Static(self.message)
        yield Button("OK", name="ok")

    def on_button_pressed(self, event):
        if event.button.name == "ok":
            self.app.pop_screen()