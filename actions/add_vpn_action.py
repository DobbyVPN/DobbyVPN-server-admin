import re
import paramiko

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
		print("Configure ssh connection:")
		server_host = input("server: ")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		auth_result = client.connect(
			server_host,
			username=input("username: "),
			password=input("password: "),
			look_for_keys=False,
			allow_agent=False)

		print("ssh conneciton on")
		_, stdout, _ = client.exec_command('cd dobbyvpn-server/ && grep OUTLINE_API_LINE= .env')
		output_lines=stdout.readlines()
		client.close()
		print("ssh conneciton off")

		if len(output_lines) != 1:
			print("Cannot find OUTLINE_API_LINE")
		else:
			output_line = output_lines[0]
			print(output_line)
			search_result = re.search(r"{\"apiUrl\":\"(\S+)\",\"certSha256\":\"(\S.+)\"}", output_line)

			if search_result is None:
				print("Invalid OUTLINE_API_LINE format")
			else:
				apiUrl = search_result.group(1).replace("127.0.0.1", server_host)
				certSha256 = search_result.group(2)
				vpn_interface = OutlineVpnInterface(apiUrl, certSha256)
				self._user_manager.add_vpn_interface(vpn_interface)
				print(f"Adding Outline VPN interface: apiUrl={apiUrl}, certSha256={certSha256}")

		return self._root_context
