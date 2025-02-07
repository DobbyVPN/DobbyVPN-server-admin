import paramiko

from typing import List, Optional


class ExternalVpnInterface:
	"""
	Wrapper around ssh connetion to the external VPN interface
	"""

	def __init__(
			self,
			interface_name: str,
			script_name: str,
			host: str,
			port: str = "22",
			username: Optional[str] = None,
			password: Optional[str] = None,
			server_workdir: str = "DobbyVPN-server/",
			server_python: str = "python3"):
		self._interface_name = interface_name
		self._script_name = script_name
		self._host = host
		self._port = port
		self._username = username
		self._password = password
		self._server_workdir = server_workdir
		self._server_python = server_python

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
			raise ExternalVpnInterfaceException("Connection error", ex)

		try:
			if user_name is None:
				command = f"cd {self._server_workdir} && {self._server_python} {self._script_name} list"
			else:
				command = f"cd {self._server_workdir} && {self._server_python} {self._script_name} list {user_name}"
			stdin, stdout, stderr = client.exec_command(command)
		except Exception as ex:
			raise ExternalVpnInterfaceException("Command execution error", ex)
		
		stdin.close()
		print("=== STDOUT ===")
		print(stdout.read().decode('utf-8'))
		print("==============")
		stdout.close()
		print("=== STDERR ===")
		print(stderr.read().decode('utf-8'))
		print("==============")
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
			raise ExternalVpnInterfaceException("Connection error", ex)

		try:
			stdin, stdout, stderr = client.exec_command(f"cd {self._server_workdir} && {self._server_python} {self._script_name} add {user_name}")
		except Exception as ex:
			raise ExternalVpnInterfaceException("Command execution error", ex)
		
		stdin.close()
		print("=== STDOUT ===")
		print(stdout.read().decode('utf-8'))
		print("==============")
		stdout.close()
		print("=== STDERR ===")
		print(stderr.read().decode('utf-8'))
		print("==============")
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
			raise ExternalVpnInterfaceException("Connection error", ex)

		try:
			stdin, stdout, stderr = client.exec_command(f"cd {self._server_workdir} && {self._server_python} {self._script_name} del {user_name}")
		except Exception as ex:
			raise ExternalVpnInterfaceException("Command execution error", ex)
		
		stdin.close()
		print("=== STDOUT ===")
		print(stdout.read().decode('utf-8'))
		print("==============")
		stdout.close()
		print("=== STDERR ===")
		print(stderr.read().decode('utf-8'))
		print("==============")
		stderr.close()

		client.close()

	def __str__(self):
		return f"{self._interface_name} on the host {self._host}"


class ExternalVpnInterfaceException(Exception):
	def __init__(self, message: str, exception: Exception):            
		super().__init__(message)
		self._message = message
		self._exception = exception

	def __str__(self):
		return f"{self._message} with cause \"{self._exception}\""
