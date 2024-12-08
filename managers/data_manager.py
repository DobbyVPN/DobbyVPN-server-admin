import uuid
import yaml
import threading

DATA_FILE = 'users.yaml'
LOCK = threading.Lock()

def load_data():
    """Загружает данные из файла users.yaml."""
    with LOCK:
        try:
            with open(DATA_FILE, 'r') as file:
                data = yaml.safe_load(file)
                if data is None:
                    data = {'users': []}
                return data
        except FileNotFoundError:
            return {'users': []}

def save_data(data):
    """Сохраняет данные в файл users.yaml."""
    with LOCK:
        with open(DATA_FILE, 'w') as file:
            yaml.dump(data, file)

def generate_id():
    """Генерирует уникальный идентификатор."""
    return uuid.uuid4().hex

def find_user_by_id(data, user_id):
    """Находит пользователя по user_id."""
    for user in data['users']:
        if user['user_id'] == user_id:
            return user
    return None

def find_user_by_name(data, user_name):
    """Находит пользователя по имени."""
    for user in data['users']:
        if user['name'] == user_name:
            return user
    return None