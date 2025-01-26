from typing import List
from user_manager.device import Device


class User:
	def __init__(self, name: str, devices: List[Device] = []):
		self._name = name
		self._devices = devices

	@property
	def name(self):
		return self._name

	@property
	def devices(self):
		return self._devices

	def add_device(self, device: Device):
		self._devices.append(device)

	def print_data(self):
		print(f"User {self._name}")

		for device in self._devices:
			print(f"- {device.dtype}")

			for key in device.keys:
				print(f"{key}")
