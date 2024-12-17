# ui/keys_view.py
from textual.events import Show
from textual.widgets import Static, Button, DataTable
from managers.data_manager import load_data
from managers.device_manager import delete_device
from ui.base_screen import BaseScreen
from ui.message_view import MessageView
from ui.rename_key_view import RenameKeyView


class KeysView(BaseScreen):
    def __init__(self, mode=None):
        super().__init__()
        self.table = None
        self.rename_input = None  # Инициализируем переменную для хранения ссылки на Input

    def compose(self):
        yield Static("Keys:")
        self.table = DataTable()
        self.table.add_column("Device ID")
        self.table.add_column("Name")
        self.table.add_column("Outline Key")
        self.refresh_keys()
        self.load_devices()
        yield self.table
        yield Button("Create a key", name="add_key", variant="success")
        yield Button("Renaming mode", name="rename", variant="primary")
        yield Button.error("Delete chosen key", name="del")
        yield Button("Back", name="back")

    def on_button_pressed(self, event):
        if event.button.name == "back":
            self.app.pop_screen()
        elif event.button.name == "del":
            self.delete_selected_device()
        elif event.button.name == "rename":
            self.app.push_screen(RenameKeyView())
        elif event.button.name == "add_key":
            from ui.add_key_view import AddKeyView
            self.app.push_screen(AddKeyView())

    def on_show(self, event: Show):
        self.refresh_keys()
        self.load_devices()

    def on_screen_resume(self):
        self.table.clear()
        self.refresh_keys()
        self.load_devices()


    def delete_selected_device(self):
        selected = self.table.cursor_row
        if selected is not None:
            row_data = self.table.get_row_at(selected)
            device_id = row_data[0]
            delete_device("admin", device_id)
            self.app.push_screen(MessageView("Success", f"Key has been deleted. ID: {device_id}"))
