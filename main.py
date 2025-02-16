from vpn_interface import ExternalVpnInterface


class AppContext:
	def __init__(self):
		self._vpn_interfaces = []

	def add_vpn_interface(self, vpn_interface: ExternalVpnInterface):
		self._vpn_interfaces.append(vpn_interface)

	@property
	def vpn_interfaces(self) -> list[ExternalVpnInterface]:
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
