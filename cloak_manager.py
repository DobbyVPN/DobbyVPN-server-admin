import sys
from dotenv import load_dotenv
from helper.parser import parse_env_json
from outline_vpn.outline_vpn import OutlineVPN, OutlineServerErrorException


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
	load_dotenv()
	API_URL, CERT_SHA256 = parse_env_json("Json")

	return OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)


def add_command():
	user_name = None

	if len(sys.argv) == 3:
		user_name = sys.argv[2]
	elif len(sys.argv) == 2:
		user_name = input("Input user name: ")
	else:
		exit(1)

	client = config_client()
	client.create_key(key_id=None, name=user_name)
		

def list_command():
	client = config_client()

	vpn_keys = client.get_keys()
	for index, key in zip(range(len(vpn_keys)), vpn_keys):
	    print(f"{index}) {key.key_id} {key.name} {key.access_url}")


def del_command():
	client = config_client()

	vpn_keys = client.get_keys()
	for index, key in zip(range(len(vpn_keys)), vpn_keys):
	    print(f"{index}) {key.key_id} {key.name} {key.access_url}")

	del_index = int(input("Enter key index: "))
	del_key = vpn_keys[del_index]
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
		callback = COMMAND_CALLBACKS[command_name]

		if callback is not None:
			callback()
		else:
			help_command()
			exit(1)
