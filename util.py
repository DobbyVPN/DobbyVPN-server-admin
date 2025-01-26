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


def outline_device(outline_key) -> Device:
	dtype = "OutlineVPN device key"
	key_data = f"""[
	"key_id": {outline_key.key_id},
	"name": {outline_key.name},
	"access_url": {outline_key.access_url}
]"""

	return Device(dtype=dtype, keys=[key_data])