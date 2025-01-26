from typing import List

from vpn_interface.vpn_interface import VpnInterface
from user_manager.user import User
from user_manager.device import Device
from util import join_users


class UserManager:
	def __init__(self):
		self._vpn_interfaces = []

	def add_user(self, user_name: str) -> User:
		result = User(user_name)

		for vpn_interface in self._vpn_interfaces:
			new_vpn_user = vpn_interface.add_user(user_name)
			result = join_users(result, new_vpn_user)

		return result

	def remove_user(self, user_name: str):
		for vpn_interface in self._vpn_interfaces:
			vpn_interface.remove_user(user_name)

	@property
	def users(self) -> List[User]:
		result = {}

		for vpn_interface in self._vpn_interfaces:
			vpn_users = vpn_interface.list_users()

			for vpn_user in vpn_users:
				if vpn_user.name not in result.keys():
					result[vpn_user.name] = User(vpn_user.name)

				result[vpn_user.name] = join_users(result[vpn_user.name], vpn_user)

		return list(result.values())

	def add_vpn_interface(self, vpn_interface: VpnInterface):
		self._vpn_interfaces.append(vpn_interface)

	@property
	def vpn_interfaces(self):
		return self._vpn_interfaces
	
