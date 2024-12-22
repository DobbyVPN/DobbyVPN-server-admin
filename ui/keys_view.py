# ui/keys_view.py

from textual.app import ComposeResult
from textual.binding import Binding
from textual.coordinate import Coordinate
from textual.events import Show
from textual.widgets import Static, Button, DataTable, Footer, Input
from textual import on

from managers.device_manager import delete_device
from vpn_interface.outline_manager import rename_outline_access_key
from ui.add_key_view import AddKeyView
from ui.base_screen import BaseScreen
from ui.message_view import MessageView


class KeysView(BaseScreen):
    table: DataTable
    rename_input: Input
    BINDINGS = [
        Binding("ctrl+a", "add", "Add new key"),
        Binding("ctrl+d", "delete", "Delete chosen key"),
        Binding("down", "focus_next", "Go down", show=False),
        Binding("up", "focus_previous", "Go up", show=False),
    ]
    def __init__(self, mode=None):
        super().__init__()
        self.new_device_id = None
        self.edit_coordinate = None
        self.edit_device_id = None
        self.rename_input_visible = False

    def action_focus_previous(self):
        self.focus_previous()

    def action_focus_next(self):
        self.focus_next()

    def action_delete(self):
        self.delete_selected_device()

    def action_add(self):
        self.app.push_screen(AddKeyView())

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Button("Create a key", name="add_key", variant="success")
        yield Button.error("Delete chosen key", name="del")
        yield Static("Keys:")
        self.table = DataTable(id="keys_table")
        self.table.add_column("Device ID")
        self.table.add_column("Name")
        self.table.add_column("Used Bytes")
        self.refresh_keys()
        self.load_devices()
        yield self.table
        # Input for in-line editing
        self.rename_input = Input(
            placeholder="Type a new name here...",
            name="rename_inline",
        )
        self.rename_input.styles.visibility = "hidden"
        yield self.rename_input
       # yield Button("Renaming mode (old)", name="rename", variant="primary")

    def show_rename_input(self, value: str):
        self.rename_input.value = value
        self.rename_input.styles.visibility = "visible"  # Показать
        self.rename_input.focus()
        self.rename_input_visible = True

    def hide_rename_input(self):
        self.rename_input.value = ""
        self.rename_input.styles.visibility = "hidden"
        self.rename_input_visible = False

    def on_button_pressed(self, event):
        if event.button.name == "del":
            self.delete_selected_device()
        elif event.button.name == "rename":
            from ui.rename_key_view import RenameKeyView
            self.app.push_screen(RenameKeyView())
        elif event.button.name == "add_key":
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
            self.refresh_keys()
            self.load_devices()
        else:
            self.app.push_screen(MessageView("Error", "No key selected."))

    @on(DataTable.CellSelected)
    def handle_cell_selected(self, event: DataTable.CellSelected) -> None:
        if event.coordinate.column == 1:
            row_idx = event.coordinate.row
            row_data = self.table.get_row_at(row_idx)
            if row_data:
                device_id = row_data[0]
                old_name = row_data[1]
                self.edit_coordinate = Coordinate(row_idx, 1)
                self.edit_device_id = device_id
                self.show_rename_input(str(old_name))
        else:
            if self.rename_input_visible:
                self.hide_rename_input()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input is self.rename_input:
            new_name = self.rename_input.value.strip()
            if self.edit_device_id and new_name:
                rename_outline_access_key(self.edit_device_id, new_name)
                if self.edit_coordinate:
                    self.table.update_cell_at(self.edit_coordinate, new_name)
                self.hide_rename_input()
                self.table.clear()
                self.refresh_keys()
                self.load_devices()
            self.edit_coordinate = None
            self.edit_device_id = None