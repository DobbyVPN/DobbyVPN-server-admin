from typing import List

from actions.action import Action, ActionContext
from user_manager.user_manager import UserManager
from vpn_interface.vpn_interface import ExternalVpnInterface

from util import *

class RootContext(ActionContext):
	def __init__(self):
		self._actions = []

	def add_action(self, action: Action):
		self._actions.append(action)

	@property
	def actions(self) -> List[Action]:
		return self._actions


class MakeUserAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Make new user"

	def execute(self) -> ActionContext:
		user_name = input("Put user name: ")
		self._user_manager.add_user(user_name)

		return self._root_context


class ListKeysAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "List all keys"

	def execute(self) -> ActionContext:
		self._user_manager.list_keys()

		return self._root_context


class DelUserAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Delete user"

	def execute(self) -> ActionContext:
		user_name = input("Put user name: ")
		self._user_manager.remove_user(user_name)

		return self._root_context


class AddInterfaceAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Add VPN interface"

	def execute(self) -> ActionContext:
		supported_vpns = [
			("outline", "users/outline_management.py", "Outline VPN"),
			("awg", "users/amneziawg_management.py", "AmneziaWG VPN"),
		]

		print("Supported server VPN interface:")
		for index, item in with_index(supported_vpns):
			print(f"{index + 1}) {item[0]}")

		user_input = input(f"Enter server VPN interface: (1..{len(supported_vpns)})")
		supported_vpn_index = int(user_input) - 1
		supported_vpn = supported_vpns[supported_vpn_index]

		vpn_interface = ExternalVpnInterface(
			supported_vpn[2],
			supported_vpn[1],
			host=input("Enter host: "),
			port=input("Enter port: "),
			username=input("Enter username: "),
			password=input("Enter password: "))
		self._user_manager.add_vpn_interface(vpn_interface)

		return self._root_context


class ListInterfacesAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "List VPN interfaces"

	def execute(self) -> ActionContext:
		for vpn_interface in self._user_manager.vpn_interfaces:
			print(vpn_interface)

		return self._root_context
