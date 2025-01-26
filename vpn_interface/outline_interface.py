from typing import List

from vpn_interface.vpn_interface import VpnInterface
from user_manager.user import User
from user_manager.device import Device
from outline_vpn.outline_vpn import OutlineVPN
from util import outline_device, outline_key_to_string


class OutlineVpnInterface:
	def __init__(self, api_url: str, cert_sha256: str):
		self._api_url = api_url
		self._cert_sha256 = cert_sha256
		self._outline_vpn = OutlineVPN(api_url=api_url, cert_sha256=cert_sha256)

	def list_users(self) -> List[User]:
		vpn_keys = self._outline_vpn.get_keys()
		indicies = range(len(vpn_keys))
		users = {}
		devices = {}

		for index, key in zip(indicies, vpn_keys):
			if key.name not in users.keys():
				new_device = outline_device()
				new_user = User(key.name, [new_device])
				users[key.name] = new_user
				devices[key.name] = new_device

			key_value = outline_key_to_string(key)
			devices[key.name].add_key(key_value)

		return list(users.values())
	
	def add_user(self, user_name: str) -> User:
		outline_key = self._outline_vpn.create_key(key_id=None, name=user_name)
		outline_dev = outline_device(outline_key)
		outline_user = User(user_name, [outline_dev])

		return outline_user

	def remove_user(self, user_name: str):
		for del_key in filter(lambda key: key.name == user_name, self._outline_vpn.get_keys()):
			self._outline_vpn.delete_key(del_key.key_id)

	def print_data(self):
		print(f"Outline VPN interface:")
		print(f"  api_url = \"{self._api_url}\"")
		print(f"  cert_sha256 = \"{self._cert_sha256}\"")
