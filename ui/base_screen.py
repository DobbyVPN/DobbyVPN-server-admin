# ui/base_screen.py
from textual.screen import Screen
from ui.message_view import MessageView
from managers.data_manager import load_data, save_data
from vpn_interface.outline_manager import get_outline_access_keys

class BaseScreen(Screen):
    def refresh_keys(self, mode = None):
        keys = get_outline_access_keys()
        if keys is None:
            self.app.push_screen(MessageView("Error", "Failed to update keys. Check your settings."))
            return
        self.update_users_yaml(keys)
        if mode == "refresh":
            self.app.push_screen(MessageView("Success", "Keys are up-to-date now."))

    def update_users_yaml(self, keys):
        data = load_data()
        user = next((u for u in data['users'] if u['user_id'] == 'admin'), None)
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

    def load_devices(self):
        data = load_data()
        devices = []
        for u in data['users']:
            if u['user_id'] == 'admin':
                devices = u.get('devices', [])
                break
        self.table.clear()  # Очистка таблицы перед загрузкой новых данных
        for d in devices:
            self.table.add_row(d['device_id'], d['device_name'], d['outline_key'])