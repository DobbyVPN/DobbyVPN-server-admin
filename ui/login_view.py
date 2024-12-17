# ui/login_view.py

import json
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Horizontal
from dotenv import set_key, load_dotenv
import os

from ui.base_screen import BaseScreen
from ui.message_view import MessageView
from vpn_interface.outline_manager import get_outline_access_keys
from managers.data_manager import load_data, save_data

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
                load_dotenv()  # Перезагрузка окружения
                # Проверим загрузку ключей
                keys = get_outline_access_keys()
                if keys is None:
                    self.app.push_screen(MessageView("Error", "Incorrect data. Failed to load keys."))
                else:
                    # Обновим users.yaml
                    from main import AdminApp
                    self.app.pop_screen()  # Закрываем LoginView
                    # main app уже запущен, обновим теперь экран:
                    # Создадим функцию, которая покажет MainView
                    # trick: можно просто push_screen MainView
                    from ui.main_view import MainView
                    self.app.push_screen(MainView())
            except json.JSONDecodeError:
                self.app.push_screen(MessageView("Error", "Incorrect JSON format"))
        elif event.button.name == "cancel":
            self.app.exit()