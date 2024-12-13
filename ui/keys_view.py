# ui/keys_view.py

from textual.screen import Screen
from textual.widgets import Static, Button, DataTable, Input
from textual.containers import Vertical, Horizontal
from managers.data_manager import load_data, save_data
from managers.device_manager import delete_device, edit_device_name
from ui.message_view import MessageView

class KeysView(Screen):
    def __init__(self, mode=None):
        super().__init__()
        self.mode = mode

    def compose(self):
        yield Static("Ключи (устройства):")
        self.table = DataTable()
        self.table.add_column("Device ID")
        self.table.add_column("Name")
        self.table.add_column("Outline Key")
        self.load_devices()
        yield self.table
        if self.mode == "delete":
            yield Button("Удалить выбранный ключ", name="del")
            yield Button("Назад", name="back")
        elif self.mode == "rename":
            yield Input(placeholder="Новое имя", name="rename_input")
            yield Button("Переименовать выбранный ключ", name="rename")
            yield Button("Назад", name="back")
        else:
            yield Button("Назад", name="back")

    def load_devices(self):
        data = load_data()
        devices = []
        for u in data['users']:
            if u['user_id'] == 'admin':
                devices = u.get('devices', [])
                break
        for d in devices:
            self.table.add_row(d['device_id'], d['device_name'], d['outline_key'])

    def on_button_pressed(self, event):
        if event.button.name == "back":
            self.app.pop_screen()
        elif event.button.name == "del":
            self.delete_selected_device()
        elif event.button.name == "rename":
            self.rename_selected_device()

    def delete_selected_device(self):
        selected = self.table.cursor_row
        if selected is not None:
            device_id = self.table.rows[selected][0]
            delete_device("admin", device_id)
            self.table.clear()
            self.load_devices()
            self.app.push_screen(MessageView("Готово", "Ключ удалён."))

    def rename_selected_device(self):
        selected = self.table.cursor_row
        if selected is not None:
            input_widget = self.query_one('Input[name="rename_input"]', Input)
            new_name = input_widget.value.strip()
            if new_name:
                device_id = self.table.rows[selected][0]
                edit_device_name("admin", device_id, new_name)
                self.table.clear()
                self.load_devices()
                self.app.push_screen(MessageView("Готово", "Ключ переименован."))

    def on_key(self, event):
        if event.key == "escape":
            self.app.pop_screen()