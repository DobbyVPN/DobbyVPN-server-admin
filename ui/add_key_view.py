# ui/add_key_view.py

from textual.screen import Screen
from textual.widgets import Static, Input, Button
from managers.device_manager import add_device
from ui.message_view import MessageView

class AddKeyView(Screen):
    def compose(self):
        yield Static("Добавление нового ключа. Введите имя:")
        self.input_name = Input(placeholder="Имя ключа")
        yield self.input_name
        yield Button("Создать", name="create",variant="primary")
        yield Button("Назад", name="cancel")

    def on_button_pressed(self, event):
        if event.button.name == "create":
            name = self.input_name.value.strip()
            if not name:
                self.app.push_screen(MessageView("Ошибка", "Нужно ввести имя"))
                return
            # Допустим add_device(user_id, device_name, key_name?)
            # Если изменен add_device для Outline ключей (key_name?), надо передать туда name
            add_device("admin", name, name)  # Если нужно, add_device("admin", name, key_name=name)
            self.app.push_screen(MessageView("Готово", f"Ключ '{name}' создан."))
            #self.app.pop_screen()
        elif event.button.name == "cancel":
            self.app.pop_screen()