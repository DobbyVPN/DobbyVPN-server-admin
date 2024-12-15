from managers.data_manager import load_data, save_data, find_user_by_id, generate_id
# from vpn_interface.wireguard_manager import generate_wireguard_keys, add_wireguard_peer, remove_wireguard_peer
from vpn_interface.outline_manager import create_outline_access_key, delete_outline_access_key

def add_device(user_id, device_name, key_name):
    """Добавляет устройство для пользователя с генерацией уникального device_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    for device in user['devices']:
        if device['device_name'] == device_name:
            raise ValueError(f"Устройство {device_name} уже существует у пользователя {user['name']}.")
    device_id = generate_id()
    # Генерация ключей

    # wg_private_key, wg_public_key = generate_wireguard_keys() - coming soon
    outline_key = create_outline_access_key(key_name)
    new_device = {
        'device_id': device_id,
        'device_name': device_name,
        #'wireguard_key': wg_public_key, - coming soon
        'outline_key': outline_key
    }
    user['devices'].append(new_device)
    save_data(data)
    # Обновление конфигураций VPN
    # add_wireguard_peer(wg_public_key) - coming soon
    return new_device

def delete_device(user_id, device_id):
    """Удаляет устройство пользователя по device_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    device = next((d for d in user['devices'] if d['device_id'] == device_id), None)
    if not device:
        raise ValueError(f"Устройство с ID {device_id} не найдено у пользователя {user['name']}.")
    # Удаление устройства из конфигураций VPN
    # remove_wireguard_peer(device['wireguard_key']) - - coming soon
    delete_outline_access_key(device_id)
    # Удаление устройства из данных пользователя
    user['devices'].remove(device)
    save_data(data)

def get_devices(user_id):
    """Возвращает список устройств пользователя по user_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    return user['devices']

def edit_device_name(user_id, device_id, new_device_name):
    """Изменяет имя устройства пользователя по device_id."""
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден.")
    for device in user['devices']:
        if device['device_name'] == new_device_name:
            raise ValueError(f"Устройство с именем {new_device_name} уже существует у пользователя {user['name']}.")
    device = next((d for d in user['devices'] if d['device_id'] == device_id), None)
    if not device:
        raise ValueError(f"Устройство с ID {device_id} не найдено у пользователя {user['name']}.")
    device['device_name'] = new_device_name
    save_data(data)