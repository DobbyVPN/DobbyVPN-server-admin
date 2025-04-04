#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "paramiko",
#     "outline-vpn-api",
# ]
# ///
import getpass
import paramiko

from typing import List, Optional


class AuthMethod:
	def auth(self):
		raise NotImplementedError()


class PasswordAuthMethod(AuthMethod):
	def __init__(self, host: str, port: str, username: str, password: str):
		self._host = host
		self._port = port
		self._username = username
		self._password = password

	def auth(self):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			client.connect(
				self._host,
				port=self._port,
				auth_strategy=paramiko.auth_strategy.Password(
					username=self._username,
					password_getter=lambda : self._password))
		except Exception as ex:
			raise VpnServerException(f"Connection error: {ex}")

		return client


class PkeyAuthMethod(AuthMethod):
	def __init__(self, username: str, host: str, port: str):
		self._username = username
		self._host = host
		self._port = port

	def auth(self):
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			client.connect(
				self._host,
				port=self._port,
				username=self._username)
		except Exception as ex:
			raise VpnServerException(f"Connection error: {ex}")

		return client


class VpnServer:
	"""
	External VPN server
	"""

	def __init__(
			self,
			name: str,
			auth_method: AuthMethod,
			image_name: str,
			image_python_path: str = ".venv/bin/python3",
			image_script_path: str = "usrmngr/main.py"):
		self._name = name
		self._auth_method=auth_method
		self._image_name = image_name
		self._image_python_path = image_python_path
		self._image_script_path = image_script_path

	def exec_command(self, client: paramiko.SSHClient, command: str) -> tuple[str, str]:
		try:
			stdin, stdout, stderr = client.exec_command(command)
		except Exception as ex:
			raise VpnServerException(f"Command execution error: {ex}")
		
		stdin.close()
		stdout_string = stdout.read().decode('utf-8')
		stderr_string = stderr.read().decode('utf-8')
		stdout.close()
		stderr.close()
		client.close()

		return (stdout_string, stderr_string)


	def healthcheck(self) -> tuple[str, str]:
		client = self._auth_method.auth()

		return self.exec_command(client, "uname -a")

	def list_keys(self, user_name: Optional[str] = None) -> tuple[str, str]:
		client = self._auth_method.auth()

		if user_name is None:
			command = f"docker exec {self._image_name} {self._image_python_path} {self._image_script_path} list"
		else:
			command = f"docker exec {self._image_name} {self._image_python_path} {self._image_script_path} list {user_name}"

		return self.exec_command(client, command)
	
	def add_user(self, user_name: str) -> tuple[str, str]:
		client = self._auth_method.auth()
		command = f"docker exec {self._image_name} {self._image_python_path} {self._image_script_path} add {user_name}"

		return self.exec_command(client, command)

	def remove_user(self, user_name: str) -> tuple[str, str]:
		client = self._auth_method.auth()
		command = f"docker exec {self._image_name} {self._image_python_path} {self._image_script_path} del {user_name}"

		return self.exec_command(client, command)

	def __str__(self):
		return f"VPN server: {self._name}"


class VpnServerException(Exception):
    pass


class KeyboardInterruptException(Exception):
	def __init__(self):
		super().__init__("Keyboard interrup exception")


class InvalidInputException(Exception):
	def __init__(self):
		super().__init__("Invalid input exception")


class AppContext:
	def __init__(self):
		self._vpn_interfaces = []

	def add_vpn_interface(self, vpn_interface: VpnServer):
		self._vpn_interfaces.append(vpn_interface)

	@property
	def vpn_interfaces(self) -> List[VpnServer]:
		return self._vpn_interfaces


def with_index(arr):
	idx = range(len(arr))

	return zip(idx, arr)


def input_string(title: str) -> str:
	try:
		value = input(f"Enter {title} ")
	except KeyboardInterrupt:
		raise KeyboardInterruptException()

	return value.strip()


def input_string_or_else(title: str, default: Optional[str]) -> Optional[str]:
	try:
		value = input(f"Enter {title}[{default}] ")
	except KeyboardInterrupt:
		raise KeyboardInterruptException()

	if value.strip():
		return value.strip()
	else:
		return default


def input_password_or_else(title: str, default: Optional[str]) -> Optional[str]:
	try:
		value = getpass.getpass(f"Enter {title}[{default}] ")
	except KeyboardInterrupt:
		raise KeyboardInterruptException()

	if value.strip():
		return value.strip()
	else:
		return default


def input_integer(title: str) -> int:
	try:
		value = input(f"Enter {title} ")
	except KeyboardInterrupt:
		raise KeyboardInterruptException()

	try:
		value_as_int = int(value)
	except ValueError:
		raise InvalidInputException()

	return value_as_int


def input_range(title: str, min_value: int, max_value: int) -> int:
	try:
		value = input(f"Enter {title}[{min_value}..{max_value}] ")
	except KeyboardInterrupt:
		raise KeyboardInterruptException()

	try:
		value_as_int = int(value)
	except ValueError:
		raise InvalidInputException()

	if value_as_int in range(min_value, max_value + 1):
		return value_as_int
	else:
		raise InvalidInputException()


def list_command(context: AppContext):
	user_name = input_string_or_else("user name", None)

	for vpn_interface in context.vpn_interfaces:
		print(vpn_interface)

		stdout, stderr = vpn_interface.list_keys(user_name)
		print(stdout.strip())
		print("STDERR:")
		print(stderr.strip())

def add_command(context: AppContext):
	user_name = input_string("user name")

	for vpn_interface in context.vpn_interfaces:
		print(vpn_interface)

		stdout, stderr = vpn_interface.add_user(user_name)
		print(stdout.strip())
		print("STDERR:")
		print(stderr.strip())


def del_command(context: AppContext):
	user_name = input_string("user name")

	for vpn_interface in context.vpn_interfaces:
		print(vpn_interface)

		stdout, stderr = vpn_interface.remove_user(user_name)
		print(stdout.strip())
		print("STDERR:")
		print(stderr.strip())


def healthcheck(vpn_interface: VpnServer):
	print(vpn_interface)

	stdout, stderr = vpn_interface.healthcheck()
	print(stdout.strip())
	print("STDERR:")
	print(stderr.strip())


def password_auth_method_builder() -> AuthMethod:
	host=input_string("host:")
	port=input_string_or_else("port:", "22")
	username=input_string_or_else("username:", None)
	password=input_password_or_else("password:", None)

	return PasswordAuthMethod(host, port, username, password)


def pkey_auth_method_builder() -> AuthMethod:
	username=input_string("username:")
	host=input_string("host:")
	port=input_string_or_else("port:", "22")

	return PkeyAuthMethod(username, host, port)


def add_vpn_command(context: AppContext):
	supported_vpns = [
		("outline-server", "Outline VPN"),
		("awg-server", "AmneziaWG VPN"),
	]

	print("Supported server VPN interfaces:")

	for index, item in with_index(supported_vpns):
		print(f"{index + 1}) {item[1]}")

	supported_vpn_index = input_range("server VPN interface", 1, len(supported_vpns)) - 1
	supported_vpn = supported_vpns[supported_vpn_index]

	supported_auth_methods = [
		(password_auth_method_builder, "Password authentification"),
		(pkey_auth_method_builder, "SSH private key authentification")
	]

	print("Supported SSH auth strategies:")
	for index, item in with_index(supported_auth_methods):
		print(f"{index + 1}) {item[1]}")

	supported_auth_index = input_range("server VPN interface", 1, len(supported_auth_methods)) - 1
	supported_auth_method = supported_auth_methods[supported_auth_index]
	auth_method = supported_auth_method[0]()

	vpn_interface = VpnServer(
		supported_vpn[1],
		auth_method=auth_method,
		image_name=supported_vpn[0])
	
	print("==== HEALTHCHECK ====")
	try:
		healthcheck(vpn_interface)
		print("Healthcheck successful, adding server")
		context.add_vpn_interface(vpn_interface)
	except Exception as ex:
		print("Healthcheck failed, skipping this server")
		print(">", ex)
	print("=====================")

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
			user_chose = input_string_or_else("action (or q to exit)", "q")
		except Exception as ex:
			print(ex)
			continue

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
				print(ex)
