import subprocess
from python_wireguard import key, Key

# заменить на свое
WG_CONFIG_FILE = '/etc/wireguard/wg0.conf'
INTERFACE_NAME = 'wg0'

def generate_wireguard_keys():
    """
    Генерирует приватный и публичный ключи WireGuard.

    Возвращает:
        tuple: Кортеж (private_key, public_key).
    """
    private_key, public_key = Key.key_pair()
    return str(private_key), str(public_key)

def add_wireguard_peer(public_key, allowed_ips, preshared_key=None):
    """
    Добавляет пир (клиента) в конфигурацию WireGuard.

    Параметры:
        public_key (str): Публичный ключ клиента.
        allowed_ips (str): Разрешенные IP-адреса для клиента (например, '10.0.0.X/32').
        preshared_key (str, optional): Предварительно разделенный ключ для дополнительной безопасности.
    """
    # TODO: добавление пира в конфигурационный файл WireGuard
    pass

def remove_wireguard_peer(public_key):
    """
    Удаляет пир из конфигурации WireGuard по публичному ключу.

    Параметры:
        public_key (str): Публичный ключ клиента, которого нужно удалить.
    """
    # TODO: удаление пира из конфигурационного файла WireGuard
    pass

def restart_wireguard_interface(interface_name=INTERFACE_NAME):
    """
    Перезапускает интерфейс WireGuard для применения изменений.

    Параметры:
        interface_name (str): Имя интерфейса WireGuard (по умолчанию задано в INTERFACE_NAME).
    """
    # TODO: перезапуск WireGuard с помощью 'wg-quick down' и 'wg-quick up'
    pass

def generate_client_config(private_key, server_public_key, allowed_ips, endpoint, dns=None, preshared_key=None):
    """
    Генерирует конфигурационный файл для клиента WireGuard.

    Параметры:
        private_key (str): Приватный ключ клиента.
        server_public_key (str): Публичный ключ сервера.
        allowed_ips (str): IP-адреса клиента в VPN-сети.
        endpoint (str): Адрес сервера WireGuard (IP и порт).
        dns (list, optional): Список DNS-серверов.
        preshared_key (str, optional): Предварительно разделенный ключ.

    Возвращает:
        str: Текст конфигурационного файла клиента.
    """
    # TODO: генерация конфигурационного файла клиента
    pass