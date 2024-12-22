# ui/add_key_view.py
from textual.binding import Binding
from textual.widgets import Static, Input, Button, Footer
from managers.device_manager import add_device
from ui.base_screen import BaseScreen
from ui.message_view import MessageView

class AddKeyView(BaseScreen):
    BINDINGS = [
        Binding("ctrl+s", "save_key", "Save Key"),
        #Binding("ctrl+b", "go_back", "Go Back"),
        #Binding("ctrl+b", "go_back", "Go Back"),
        Binding("down", "focus_next", "Go down", show=False),
        Binding("up", "focus_previous", "Go up", show=False)
    ]

    def action_focus_previous(self):
        self.focus_previous()

    def action_focus_next(self):
        self.focus_next()

    def compose(self):
        yield Footer()
        yield Static("Creating a new key. Enter name:")
        self.input_name = Input(placeholder="Key name")
        yield self.input_name
        yield Button("Create", name="create",variant="primary")
        yield Button("Back", name="cancel")



    def create_key(self):
        name = self.input_name.value.strip()
        if not name:
            self.app.push_screen(MessageView("Error", "You must enter a name"))
            return
        new_device = add_device("admin", name, name)

        self.dismiss(result=new_device["device_id"])

    def action_save_key(self):
        self.create_key()

    def on_button_pressed(self, event):
        if event.button.name == "create":
            self.create_key()
        elif event.button.name == "cancel":
            self.app.pop_screen()