from typing import List

from actions.action import Action, ActionContext
from user_manager.user_manager import UserManager
from vpn_interface.outline_interface import OutlineVpnInterface


class AddVpnInterfaceActionContext(ActionContext):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._actions = [
			AddOutlineInterfaceAction(user_manager, root_context)
		]
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def actions(self) -> List[Action]:
		return self._actions


class AddOutlineInterfaceAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Add Outline VPN interface"

	def execute(self) -> ActionContext:
		apiUrl = input("apiUrl: ")
		certSha256 = input("certSha256: ")
		vpn_interface = OutlineVpnInterface(apiUrl, certSha256)
		self._user_manager.add_vpn_interface(vpn_interface)

		return self._root_context