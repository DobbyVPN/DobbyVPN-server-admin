import sys
from dotenv import load_dotenv
from helper.parser import parse_env_json
from outline_vpn.outline_vpn import OutlineVPN


def help_command():
	program_name = sys.argv[0]
	help_message = f"""{program_name} help
	prints script informations
{program_name} add [ user_name ]
	adds new user to the Outline and returns key and cloak client config.
	if user_name is not set, script asks it from the stdout
{program_name} list
	prints list of all keys
{program_name} del
	runs key deletion.
	1) prints all keys
	2) requests key number to delete
	3) sends delete verification
"""

	print(help_message)


def config_client():
	print("=== Load Cloak client from config ===")
	load_dotenv()
	API_URL, CERT_SHA256 = parse_env_json("Json")
	print("=== Loaded ===")

	return OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)


def add_command():
	user_name = None

	if len(sys.argv) == 3:
		user_name = sys.argv[2]
	elif len(sys.argv) == 2:
		user_name = input("Input user name: ")
	else:
		help_command()
		exit(1)

	client = config_client()
	client.create_key(key_id=None, name=user_name)


def list_command():
	if len(sys.argv) != 2:
		help_command()
		exit(1)

	client = config_client()

	print("Cloak client keys:")
	vpn_keys = client.get_keys()
	for index, key in zip(range(len(vpn_keys)), vpn_keys):
	    print(f"{index}) {key.key_id} {key.name} {key.access_url}")


def del_command():
	if len(sys.argv) != 2:
		help_command()
		exit(1)

	client = config_client()
	vpn_keys = client.get_keys()

	for index, key in zip(range(len(vpn_keys)), vpn_keys):
	    print(f"{index}) {key.key_id} {key.name} {key.access_url}")

	try:
		del_index = int(input("Enter key index: "))
		del_key = vpn_keys[del_index]
	except ValueError:
		raise ValueError(f"Key must be integer in the 0..{len(vpn_keys) - 1} range")
	except IndexError:
		raise ValueError(f"Key must be integer in the 0..{len(vpn_keys) - 1} range")
	
	client.delete_key(del_key.key_id)


COMMAND_CALLBACKS = {
	"help": help_command,
	"add": add_command,
	"list": list_command,
	"del": del_command,
}


if __name__ == "__main__":
	if len(sys.argv) == 1:
		help_command()
	else:
		command_name = sys.argv[1]
		command_callback = COMMAND_CALLBACKS[command_name]

		if command_callback is not None:
			command_callback()
		else:
			help_command()
			exit(1)
