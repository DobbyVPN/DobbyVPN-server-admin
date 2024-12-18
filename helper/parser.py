import os
import json
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()

def parse_env_json(key: str):
    """
    Считывает JSON-строку из переменной окружения key и парсит её.
    Возвращает значения api_url и cert.
    """
    # Считываем значение переменной окружения
    json_string = os.getenv(key)
    if not json_string:
        raise ValueError(f"Переменная '{key}' не найдена или пуста")

    try:
        # Парсим строку в словарь
        data = json.loads(json_string)
        api_url = data.get("apiUrl")
        cert = data.get("certSha256")
        print(api_url, '\n')
        print(cert)
        if not api_url or not cert:
            raise ValueError("JSON должен содержать оба ключа: 'apiUrl' и 'certSha256'")
        return api_url, cert
    except json.JSONDecodeError:
        raise ValueError("Некорректный формат JSON в переменной окружения")