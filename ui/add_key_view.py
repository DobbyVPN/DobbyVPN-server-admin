# ui/add_key_view.py

from textual.widgets import Static, Input, Button
from managers.device_manager import add_device
from ui.base_screen import BaseScreen
from ui.message_view import MessageView

class AddKeyView(BaseScreen):
    def compose(self):
        yield Static("Creating a new key. Enter name:")
        self.input_name = Input(placeholder="Key name")
        yield self.input_name
        yield Button("Create", name="create",variant="primary")
        yield Button("Back", name="cancel")

    def on_button_pressed(self, event):
        if event.button.name == "create":
            name = self.input_name.value.strip()
            if not name:
                self.app.push_screen(MessageView("Error", "You must enter a name"))
                return
            # Допустим add_device(user_id, device_name, key_name?)
            # Если изменен add_device для Outline ключей (key_name?), надо передать туда name
            add_device("admin", name, name)  # Если нужно, add_device("admin", name, key_name=name)
            self.app.push_screen(MessageView("Success", f"Key '{name}' has been created."))
            #self.app.pop_screen()
        elif event.button.name == "cancel":
            self.app.pop_screen()