from user_manager.user import User
from user_manager.device import Device


def with_index(arr):
	idx = range(len(arr))

	return zip(idx, arr)


def join_users(user1: User, user2: User) -> User:
	joined_devices = []
	joined_devices.extend(user1.devices)
	joined_devices.extend(user2.devices)

	return User(user1.name, joined_devices)


def outline_device() -> Device:
	dtype = "OutlineVPN device key"

	return Device(dtype=dtype, keys=[])


def outline_key_to_string(key) -> str:
	return "{key_id} \"{name}\" \"{access_url}\" {used_bytes} {data_limit}".format(
		key_id=key.key_id,
		name=key.name,
		access_url=key.access_url,
		used_bytes=key.used_bytes,
		data_limit=key.data_limit)