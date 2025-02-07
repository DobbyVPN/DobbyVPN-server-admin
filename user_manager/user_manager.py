from typing import List, Optional
from vpn_interface.vpn_interface import ExternalVpnInterface


class UserManager:
	def __init__(self):
		self._vpn_interfaces = []

	def list_keys(self, user_name: Optional[str] = None):
		for vpn_interface in self._vpn_interfaces:
			vpn_interface.list_keys(user_name)

	def add_user(self, user_name: str):
		for vpn_interface in self._vpn_interfaces:
			vpn_interface.add_user(user_name)

	def remove_user(self, user_name: str):
		for vpn_interface in self._vpn_interfaces:
			vpn_interface.remove_user(user_name)

	def add_vpn_interface(self, vpn_interface: ExternalVpnInterface):
		self._vpn_interfaces.append(vpn_interface)

	@property
	def vpn_interfaces(self):
		return self._vpn_interfaces
	
