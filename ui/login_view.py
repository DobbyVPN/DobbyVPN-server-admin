# ui/login_view.py
#UNUSED
import json
import os
import time

from textual.widgets import Static, Input, Button
from textual.containers import Horizontal
from dotenv import set_key, load_dotenv

from managers.data_manager import load_data, save_data
from ui.base_screen import BaseScreen
from ui.message_view import MessageView
from vpn_interface.outline_manager import get_outline_access_keys

class LoginView(BaseScreen):
    def compose(self):
        yield Static("Enter JSON with apiUrl and certSha256:")
        # Пример: {"apiUrl":"https://195.201.111.36:43180/KlvPGo_8P1ZDCmGmrHxxgg","certSha256":"..."}
        self.json_input = Input(placeholder='{"apiUrl":"...","certSha256":"..."}')
        yield self.json_input
        yield Horizontal(
            Button("Save", name="save"),
            Button("Cancel", name="cancel")
        )

    def update_users_yaml_with_keys(self, keys):
        data = load_data()
        # Предположим один пользователь admin
        user = None
        for u in data['users']:
            if u['user_id'] == 'admin':
                user = u
                break
        if not user:
            user = {'user_id': 'admin', 'name': 'admin_user', 'devices': []}
            data['users'].append(user)
        user['devices'].clear()
        # Заполняем devices данными из keys
        for k in keys:
            device = {
                'device_id': k.key_id,
                'device_name': k.name,
                'outline_key': k.access_url
            }
            user['devices'].append(device)
        save_data(data)

    def on_button_pressed(self, event):
        if event.button.name == "save":
            val = self.json_input.value.strip()
            if not val:
                self.app.push_screen(MessageView("Error", "You need to enter JSON"))
                return
            try:
                data = json.loads(val)
                api_url = data.get("apiUrl")
                cert = data.get("certSha256")
                if not api_url or not cert:
                    self.app.push_screen(MessageView("Error", "JSON must contain both apiUrl and certSha256"))
                    return
                set_key(".env", "OUTLINE_API_URL", api_url)
                set_key(".env", "OUTLINE_CERT_SHA256", cert)
                #time.sleep(1)
                load_dotenv()  # Перезагрузка окружения
                from vpn_interface.outline_manager import get_outline_access_keys
                #self.app.outline_vpn = OutlineVPN(api_url=os.getenv("OUTLINE_API_URL"), cert_sha256=os.getenv("OUTLINE_CERT_SHA256"))
                # Проверим загрузку ключей
                keys = get_outline_access_keys()
                if keys is None:
                    self.app.push_screen(MessageView("Error", "Incorrect data. Failed to load keys."))
                else:
                    self.update_users_yaml_with_keys(keys)
                    self.app.push_screen(MessageView("Success", "Correct JSON format"))
                    # Обновим users.yaml
                    from main import AdminApp
                    self.app.pop_screen()  # Закрываем LoginView
                    # main app уже запущен, обновим теперь экран:
                    from ui.main_view import MainView
                    self.app.push_screen(MainView())
            except json.JSONDecodeError:
                self.app.push_screen(MessageView("Error", "Incorrect JSON format"))
        elif event.button.name == "cancel":
            self.app.exit()