# main.py
import os
from shutil import Error

from dotenv import load_dotenv
load_dotenv()
from textual.app import App
from ui.login_view import LoginView
from ui.main_view import MainView
from ui.message_view import MessageView
from vpn_interface.outline_manager import get_outline_access_keys
from managers.data_manager import load_data, save_data



class AdminApp(App):
    TITLE = "Outline Admin Interface"
    # main.py
    async def on_ready(self):
        print("Приложение начало работу")
        from helper.parser import parse_env_json
        api_url, cert = parse_env_json("Json")
        if not api_url or not cert:
            raise Error("api_url and cert weren't found in .env file.")
            #await self.push_screen(LoginView())
        else:
            print(f"Переменные окружения найдены: API_URL={api_url}, CERT={cert}")
            keys = get_outline_access_keys()
            if keys is None:
                print("Не удалось загрузить ключи. Ошибка API.")
                await self.push_screen(
                    MessageView("Ошибка", "Не удалось загрузить ключи Outline. Проверьте API URL и CERT."))
            else:
                self.update_users_yaml_with_keys(keys)
                print("Ключи успешно загружены, переход на MainView.")
                await self.push_screen(MainView())

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


if __name__ == "__main__":
    app = AdminApp()
    app.run()