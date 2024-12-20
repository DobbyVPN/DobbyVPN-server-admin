# ui/keys_view.py
from textual.binding import Binding
from textual.events import Show
from textual.widgets import Static, Button, DataTable, Footer
from managers.device_manager import delete_device
from ui.base_screen import BaseScreen
from ui.message_view import MessageView
from ui.rename_key_view import RenameKeyView


class KeysView(BaseScreen):
    table = DataTable()

    BINDINGS = [
        Binding("ctrl+d","delete","Delete chosen key"),
        Binding("down", "focus_next", "Go down", show=False),
        Binding("up", "focus_previous", "Go up", show=False)
    ]

    def action_focus_previous(self):
        self.focus_previous()

    def action_focus_next(self):
        self.focus_next()

    def action_delete(self):
        self.delete_selected_device()

    def __init__(self, mode=None):
        super().__init__()
        self.table = None
        self.rename_input = None
        self.new_device_id = None

    def compose(self):
        yield Footer()
        yield Button("Create a key", name="add_key", variant="success")
        yield Static("Keys:")
        self.table = DataTable()
        self.table.add_column("Device ID")
        self.table.add_column("Name")
        self.table.add_column("Used Bytes")
        #self.table.add_column("Outline Key")
        self.refresh_keys()
        self.load_devices()
        yield self.table

        yield Button("Renaming mode", name="rename", variant="primary")
        yield Button.error("Delete chosen key", name="del")

    def on_button_pressed(self, event):
        if event.button.name == "del":
            self.delete_selected_device()
        elif event.button.name == "rename":
            self.app.push_screen(RenameKeyView())
        elif event.button.name == "add_key":
            from ui.add_key_view import AddKeyView
            self.app.push_screen(AddKeyView())

    def on_show(self, event: Show):
        self.refresh_keys()
        self.load_devices()

    def on_screen_resume(self, return_value = None):
        if len(self.app.screen_stack) >= 2:
            prev_screen = self.app.screen_stack[-2]
            if hasattr(prev_screen, "result") and prev_screen.result:
                self.new_device_id = prev_screen.result
        self.table.clear()
        self.refresh_keys()
        self.load_devices()
        if self.new_device_id:
            self.select_added_device(self.new_device_id)
            self.new_device_id = None

    def select_added_device(self, device_id):
        for index, row in enumerate(self.table.rows):
            row_device_id = row[0]
            if row_device_id == device_id:
                self.table.cursor_type = "row"
                self.table.cursor_row = index
                break

    def delete_selected_device(self):
        selected = self.table.cursor_row
        if selected is not None:
            row_data = self.table.get_row_at(selected)
            device_id = row_data[0]
            delete_device("admin", device_id)
            #self.app.push_screen(MessageView("Success", f"Key has been deleted. ID: {device_id}"))
            #self.app.pop_screen()
            self.refresh_keys()
            self.load_devices()
        else:
            self.app.push_screen(MessageView("Error", "No key selected."))
