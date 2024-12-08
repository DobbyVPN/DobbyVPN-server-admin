# managers/user_manager.py

from managers.data_manager import load_data, save_data, find_user_by_id, find_user_by_name, generate_id

def add_user(user_name):
    """Добавляет нового пользователя с уникальным user_id."""
    data = load_data()
    if find_user_by_name(data, user_name):
        raise ValueError(f"Пользователь {user_name} уже существует.")
    user_id = generate_id()
    new_user = {'user_id': user_id, 'name': user_name, 'devices': []}
    data['users'].append(new_user)
    save_data(data)
    return new_user

def delete_user(user_id):
    """Удаляет пользователя и все его устройства по user_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    data['users'].remove(user)
    save_data(data)

def get_users():
    """Возвращает список всех пользователей."""
    data = load_data()
    return data['users']

def edit_user_name(user_id, new_name):
    """Изменяет имя пользователя по user_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    if find_user_by_name(data, new_name):
        raise ValueError(f"Пользователь с именем {new_name} уже существует.")
    user['name'] = new_name
    save_data(data)