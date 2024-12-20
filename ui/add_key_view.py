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

    def action_save_key(self):
        name = self.input_name.value.strip()
        if not name:
            self.app.push_screen(MessageView("Error", "You must enter a name"))
            return
        # Допустим add_device(user_id, device_name, key_name?)
        # Если изменен add_device для Outline ключей (key_name?), надо передать туда name
        add_device("admin", name, name)  # Если нужно, add_device("admin", name, key_name=name)
        self.app.push_screen(MessageView("Success", f"Key '{name}' has been created."))

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