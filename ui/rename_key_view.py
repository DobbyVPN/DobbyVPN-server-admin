#ui/keys_view.py
from textual.binding import Binding
from textual.widgets import Static, Button, DataTable, Input
from ui.base_screen import BaseScreen
from ui.message_view import MessageView
from vpn_interface.outline_manager import rename_outline_access_key




class RenameKeyView(BaseScreen):
    def __init__(self, mode=None):
        super().__init__()
        self.mode = mode
        self.rename_input = None

    BINDINGS=[
        Binding("down", "focus_next", "Go down", show=False),
        Binding("up", "focus_previous", "Go up", show=False)
    ]

    def action_focus_previous(self):
        self.focus_previous()

    def action_focus_next(self):
        self.focus_next()

    def compose(self):
        yield Static("Keys:")
        self.table = DataTable()
        self.table.add_column("Device ID")
        self.table.add_column("Name")
        self.table.add_column("Outline Key")
        self.load_devices()
        yield self.table
        self.rename_input = Input(placeholder="New name", name="rename_input")
        yield self.rename_input
        yield Button("Rename chosen key", name="rename")
        yield Button("Back", name="back")


    def rename_selected_device(self):
        selected = self.table.cursor_row
        if selected is not None:
            if self.rename_input is None:
                self.app.push_screen(MessageView("Error", "Input field not found."))
                return
            new_name = self.rename_input.value.strip()
            if new_name:
                row_data = self.table.get_row_at(selected)
                device_id = row_data[0]
                rename_outline_access_key(device_id, new_name)
                self.table.clear()
                self.refresh_keys()
                self.load_devices()
                #self.app.push_screen(MessageView("Ready", "The key has been renamed."))
            else:
                self.app.push_screen(MessageView("Error", "The new name cannot be empty."))
        else:
            self.app.push_screen(MessageView("Error", "No key selected."))

    def on_button_pressed(self, event):
        if event.button.name == "rename":
            self.rename_selected_device()
            self.refresh_keys()
        if event.button.name == "back":
            self.app.pop_screen()
