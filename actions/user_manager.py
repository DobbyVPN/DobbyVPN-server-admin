from typing import List

class Device:
	def __init__(self, dtype: str, keys: List[str]):
		self._dtype = dtype
		self._keys = keys

	@property
	def dtype(self) -> str:
		return self._dtype

	@property
	def keys(self) -> List[str]:
		return self._keys


class User:
	def __init__(self, name: str):
		self._devices = []
		self._name = name

	@property
	def name(self):
		return self._name

	def print_data(self):
		print(f"User {self._name}")

		for device in self._devices:
			print(f"- {device.dtype}")

			for key in device.keys:
				print(f"-- {key}")


class UserManager:
	def __init__(self):
		self._users = []

	def add_user(self, user_name: str) -> User:
		new_user = User(user_name)
		self._users.append(new_user)

		return new_user

	def remove_user(self, user_index: int):
		self._users.pop(user_index)

	@property
	def users(self):
		return self._users
