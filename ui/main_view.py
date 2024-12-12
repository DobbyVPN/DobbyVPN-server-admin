# ui/main_view.py

from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical
from ui.keys_view import KeysView
from ui.message_view import MessageView
from vpn_interface.outline_manager import get_outline_access_keys
from managers.data_manager import load_data, save_data

class MainView(Screen):
    def compose(self):
        yield Static("Главное меню:")
        yield Vertical(
            Button("Показать ключи", name="show_keys"),
            Button("Обновить ключи с сервера Outline", name="refresh"),
            Button("Добавить ключ", name="add_key"),
            Button("Удалить ключ", name="del_key"),
            Button("Переименовать ключ", name="rename_key"),
            Button("Выход", name="exit")
        )

    def on_button_pressed(self, event):
        if event.button.name == "show_keys":
            self.app.push_screen(KeysView())
        elif event.button.name == "refresh":
            self.refresh_keys()
        elif event.button.name == "add_key":
            from ui.add_key_view import AddKeyView
            self.app.push_screen(AddKeyView())
        elif event.button.name == "del_key":
            # Откроем KeysView с режимом удаления
            self.app.push_screen(KeysView(mode="delete"))
        elif event.button.name == "rename_key":
            self.app.push_screen(KeysView(mode="rename"))
        elif event.button.name == "exit":
            self.app.exit()

    def refresh_keys(self):
        keys = get_outline_access_keys()
        if keys is None:
            self.app.push_screen(MessageView("Ошибка", "Не удалось обновить ключи. Проверьте настройки."))
            return
        self.update_users_yaml(keys)
        self.app.push_screen(MessageView("Успех", "Ключи обновлены."))

    def update_users_yaml(self, keys):
        data = load_data()
        user = None
        for u in data['users']:
            if u['user_id'] == 'admin':
                user = u
                break
        if not user:
            user = {'user_id': 'admin', 'name': 'admin_user', 'devices': []}
            data['users'].append(user)
        user['devices'].clear()
        for k in keys:
            device = {
                'device_id': k.key_id,
                'device_name': k.name,
                'outline_key': k.access_url
            }
            user['devices'].append(device)
        save_data(data)