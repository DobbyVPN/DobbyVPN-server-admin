from python_wireguard import key, Key

WG_CONFIG_FILE = '/etc/wireguard/wg0.conf'
INTERFACE_NAME = 'wg0'

def generate_wireguard_keys():

    private_key, public_key = Key.key_pair()
    return str(private_key), str(public_key)

def add_wireguard_peer(public_key, allowed_ips, preshared_key=None):

    # TODO:
    pass

def remove_wireguard_peer(public_key):

    # TODO:
    pass

def restart_wireguard_interface(interface_name=INTERFACE_NAME):

    # TODO:
    pass

def generate_client_config(private_key, server_public_key, allowed_ips, endpoint, dns=None, preshared_key=None):

    # TODO:
    pass