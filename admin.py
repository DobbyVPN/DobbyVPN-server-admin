#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "paramiko",
#     "outline-vpn-api",
# ]
# ///
import paramiko

from typing import List, Optional


class ExternalVpnInterface:
	"""
	Wrapper around ssh connetion to the external VPN interface
	"""

	def __init__(
			self,
			interface_name: str,
			host: str,
			port: str = "22",
			username: Optional[str] = None,
			password: Optional[str] = None):
		self._interface_name = interface_name
		self._host = host
		self._port = port
		self._username = username
		self._password = password

	def list_keys(self, user_name: Optional[str] = None):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			client.connect(
				self._host,
				port=self._port,
				username=self._username,
				password=self._password,
				look_for_keys=False,
				allow_agent=False)
		except Exception as ex:
			print(f"Connection error: {ex}")

		try:
			if user_name is None:
				command = f"docker exec awg-server .venv/bin/python3 usrmngr/main.py list"
			else:
				command = f"docker exec awg-server .venv/bin/python3 usrmngr/main.py list {user_name}"

			stdin, stdout, stderr = client.exec_command(command)
		except Exception as ex:
			print(f"Command execution error: {ex}")
		
		stdin.close()
		print("stdout:")
		print(stdout.read().decode('utf-8'))
		stdout.close()
		print("stderr")
		print(stderr.read().decode('utf-8'))
		stderr.close()

		client.close()
	
	def add_user(self, user_name: str):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			client.connect(
				self._host,
				port=self._port,
				username=self._username,
				password=self._password,
				look_for_keys=False,
				allow_agent=False)
		except Exception as ex:
			print(f"Connection error: {ex}")

		try:
			command = f"docker exec awg-server .venv/bin/python3 usrmngr/main.py add {user_name}"

			stdin, stdout, stderr = client.exec_command(command)
		except Exception as ex:
			print(f"Command execution error: {ex}")
		
		stdin.close()
		print("stdout")
		print(stdout.read().decode('utf-8'))
		stdout.close()
		print("stderr")
		print(stderr.read().decode('utf-8'))
		stderr.close()

		client.close()

	def remove_user(self, user_name: str):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			client.connect(
				self._host,
				port=self._port,
				username=self._username,
				password=self._password,
				look_for_keys=False,
				allow_agent=False)
		except Exception as ex:
			print(f"Connection error: {ex}")

		try:
			command = f"docker exec awg-server .venv/bin/python3 usrmngr/main.py del {user_name}"

			stdin, stdout, stderr = client.exec_command(command)
		except Exception as ex:
			print(f"Command execution error: {ex}")
		
		stdin.close()
		print("stdout")
		print(stdout.read().decode('utf-8'))
		stdout.close()
		print("stderr")
		print(stderr.read().decode('utf-8'))
		stderr.close()

		client.close()

	def __str__(self):
		return f"{self._interface_name} on the host {self._host}"


class AppContext:
	def __init__(self):
		self._vpn_interfaces = []

	def add_vpn_interface(self, vpn_interface: ExternalVpnInterface):
		self._vpn_interfaces.append(vpn_interface)

	@property
	def vpn_interfaces(self) -> List[ExternalVpnInterface]:
		return self._vpn_interfaces


def with_index(arr):
	idx = range(len(arr))

	return zip(idx, arr)


def list_command(context: AppContext):
	for vpn_interface in context.vpn_interfaces:
		vpn_interface.list_keys()


def add_command(context: AppContext):
	user_name = input("Enter user name: ")

	for vpn_interface in context.vpn_interfaces:
		vpn_interface.add_user(user_name)


def del_command(context: AppContext):
	user_name = input("Enter user name: ")

	for vpn_interface in context.vpn_interfaces:
		vpn_interface.remove_user(user_name)


def add_vpn_command(context: AppContext):
	supported_vpns = [
		# ("outline", "users/outline_management.py", "Outline VPN"),
		("awg", "AmneziaWG VPN"),
	]

	print("Supported server VPN interfaces:")

	for index, item in with_index(supported_vpns):
		print(f"{index + 1}) {item[0]}")

	user_input = input(f"Enter server VPN interface: ")
	supported_vpn_index = int(user_input) - 1
	supported_vpn = supported_vpns[supported_vpn_index]

	vpn_interface = ExternalVpnInterface(
		supported_vpn[1],
		host=input("Enter host: "),
		port=input("Enter port: "),
		username=input("Enter username: "),
		password=input("Enter password: "))
	context.add_vpn_interface(vpn_interface)


def list_vpn_command(context: AppContext):
	for vpn_interface in context.vpn_interfaces:
		print(vpn_interface)


if __name__ == "__main__":
	app_context = AppContext()
	commands = [
		("List keys", list_command), 
		("Add user", add_command), 
		("Remove user", del_command), 
		("Add VPN server", add_vpn_command), 
		("List VPN servers", list_vpn_command)]

	while True:
		for index, command in with_index(commands):
			print(f"[{index + 1}] {command[0]}")

		try:
			user_chose = input("Select action or write down 'q' to exit: ")
		except KeyboardInterrupt:
			print("\nKeyboardInterrupt: exit user cycle")
			break

		if user_chose == 'q':
			break
		else:
			try:
				action_index = int(user_chose) - 1
				user_action = commands[action_index][1]
			except Exception:
				print("Invalid input")
				continue

			try:
				user_action(app_context)
			except Exception as ex:
				print(f"Exception during user action execute: {ex}")
