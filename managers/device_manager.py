from managers.data_manager import load_data, save_data, find_user_by_id, generate_id
# from vpn_interface.wireguard_manager import generate_wireguard_keys, add_wireguard_peer, remove_wireguard_peer
from vpn_interface.outline_manager import create_outline_access_key, delete_outline_access_key

def add_device(user_id, device_name, key_name):
    data = load_data()
    user = find_user_by_id(data, user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    for device in user['devices']:
        if device['device_name'] == device_name:
            raise ValueError(f"Device {device_name} already exists.")
    device_id = generate_id()


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
    # add_wireguard_peer(wg_public_key) - coming soon
    return new_device

def delete_device(user_id, device_id):
    data = load_data()
    user = find_user_by_id(data, user_id)
    device = next((d for d in user['devices'] if d['device_id'] == device_id), None)
    # remove_wireguard_peer(device['wireguard_key']) - - coming soon
    delete_outline_access_key(device_id)
    user['devices'].remove(device)
    save_data(data)

def get_devices(user_id):
    data = load_data()
    user = find_user_by_id(data, user_id)
    return user['devices']

def edit_device_name(user_id, device_id, new_device_name):
    data = load_data()
    user = find_user_by_id(data, user_id)
    for device in user['devices']:
        if device['device_name'] == new_device_name:
            raise ValueError(f"Device with name {new_device_name} already exists: user: {user['name']}.")
    device = next((d for d in user['devices'] if d['device_id'] == device_id), None)
    device['device_name'] = new_device_name
    save_data(data)