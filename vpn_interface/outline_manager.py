"""
outline_manager.py

API FOR OUTLINE VPN SERVER
"""

import os
import typing
import urllib.parse
import requests
from dotenv import load_dotenv
from urllib3 import PoolManager
from dataclasses import dataclass

from helper.parser import parse_env_json

load_dotenv(dotenv_path="../.env")
# --------------------------------------------
# Outline server connetcing settings
# --------------------------------------------
API_URL, CERT_SHA256 = parse_env_json("Json")
#print(API_URL, CERT_SHA256)

UNABLE_TO_GET_METRICS_ERROR = "Unable to get metrics"

@dataclass
class OutlineKey:
    """
    Describes a key in the Outline server
    """
    key_id: str
    name: str
    password: str
    port: int
    method: str
    access_url: str
    used_bytes: int
    data_limit: typing.Optional[int]

    def __init__(self, response: dict, metrics: dict = None):
        self.key_id = response.get("id")
        self.name = response.get("name")
        self.password = response.get("password")
        self.port = response.get("port")
        self.method = response.get("method")
        self.access_url = response.get("accessUrl")
        self.used_bytes = (
            metrics.get("bytesTransferredByUserId").get(response.get("id"))
            if (metrics and "bytesTransferredByUserId" in metrics)
            else 0
        )
        self.data_limit = response.get("dataLimit", {}).get("bytes")

class OutlineServerErrorException(Exception):
    pass

class OutlineLibraryException(Exception):
    pass

class _FingerprintAdapter(requests.adapters.HTTPAdapter):

    def __init__(self, fingerprint=None, **kwargs):
        self.fingerprint = str(fingerprint)
        super(_FingerprintAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            assert_fingerprint=self.fingerprint,
        )

class OutlineVPN:

    def __init__(self, api_url: str, cert_sha256: str):
        self.api_url = api_url
        if cert_sha256:
            session = requests.Session()
            session.mount("https://", _FingerprintAdapter(cert_sha256))
            self.session = session
        else:
            raise OutlineLibraryException(
                "No certificate SHA256 provided. Running without certificate is no longer supported."
            )

    def get_keys(self, timeout: int = None):
        response = self.session.get(
            f"{self.api_url}/access-keys/", verify=False, timeout=timeout
        )
        if response.status_code == 200 and "accessKeys" in response.json():
            response_metrics = self.session.get(
                f"{self.api_url}/metrics/transfer", verify=False
            )
            if (
                response_metrics.status_code >= 400
                or "bytesTransferredByUserId" not in response_metrics.json()
            ):
                raise OutlineServerErrorException(UNABLE_TO_GET_METRICS_ERROR)

            response_json = response.json()
            result = []
            for key in response_json.get("accessKeys", []):
                result.append(OutlineKey(key, response_metrics.json()))
            return result
        raise OutlineServerErrorException(f"Unable to retrieve keys {response.status_code}")

    def get_key(self, key_id: str, timeout: int = None) -> OutlineKey:
        response = self.session.get(
            f"{self.api_url}/access-keys/{key_id}", verify=False, timeout=timeout
        )
        if response.status_code == 200:
            key = response.json()

            response_metrics = self.session.get(
                f"{self.api_url}/metrics/transfer", verify=False, timeout=timeout
            )
            if (
                response_metrics.status_code >= 400
                or "bytesTransferredByUserId" not in response_metrics.json()
            ):
                raise OutlineServerErrorException(UNABLE_TO_GET_METRICS_ERROR)

            return OutlineKey(key, response_metrics.json())
        else:
            raise OutlineServerErrorException("Unable to get key")

    def create_key(
        self,
        key_id: str = None,
        name: str = None,
        method: str = None,
        password: str = None,
        data_limit: int = None,
        port: int = None,
        timeout: int = None,
    ) -> OutlineKey:
        payload = {}
        if name:
            payload["name"] = name
        if method:
            payload["method"] = method
        if password:
            payload["password"] = password
        if data_limit:
            payload["limit"] = {"bytes": data_limit}
        if port:
            payload["port"] = port
        if key_id:
            payload["id"] = key_id
            response = self.session.put(
                f"{self.api_url}/access-keys/{key_id}",
                verify=False,
                json=payload,
                timeout=timeout,
            )
        else:
            response = self.session.post(
                f"{self.api_url}/access-keys",
                verify=False,
                json=payload,
                timeout=timeout,
            )

        if response.status_code == 201:
            key = response.json()
            outline_key = OutlineKey(key)
            return outline_key

        raise OutlineServerErrorException(f"Unable to create key. {response.text}")

    def delete_key(self, key_id: str, timeout: int = None) -> bool:
        response = self.session.delete(
            f"{self.api_url}/access-keys/{key_id}", verify=False, timeout=timeout
        )
        if response.status_code == 204:
            return response.status_code == 204
        raise OutlineServerErrorException(f"Unable to delete key. {response.text}")

    def rename_key(self, key_id: str, name: str, timeout: int = None):
        files = {
            "name": (None, name),
        }

        response = self.session.put(
            f"{self.api_url}/access-keys/{key_id}/name",
            files=files,
            verify=False,
            timeout=timeout,
        )
        return response.status_code == 204

    def add_data_limit(self, key_id: str, limit_bytes: int, timeout: int = None) -> bool:
        data = {"limit": {"bytes": limit_bytes}}
        response = self.session.put(
            f"{self.api_url}/access-keys/{key_id}/data-limit",
            json=data,
            verify=False,
            timeout=timeout,
        )
        return response.status_code == 204

    def delete_data_limit(self, key_id: str, timeout: int = None) -> bool:
        response = self.session.delete(
            f"{self.api_url}/access-keys/{key_id}/data-limit",
            verify=False,
            timeout=timeout,
        )
        return response.status_code == 204

    def get_transferred_data(self, timeout: int = None):
        response = self.session.get(
            f"{self.api_url}/metrics/transfer", verify=False, timeout=timeout
        )
        if (
            response.status_code >= 400
            or "bytesTransferredByUserId" not in response.json()
        ):
            raise OutlineServerErrorException(UNABLE_TO_GET_METRICS_ERROR)
        return response.json()

    def get_server_information(self, timeout: int = None):
        response = self.session.get(
            f"{self.api_url}/server", verify=False, timeout=timeout
        )
        if response.status_code != 200:
            raise OutlineServerErrorException(
                "Unable to get information about the server"
            )
        return response.json()

    def set_server_name(self, name: str, timeout: int = None) -> bool:
        data = {"name": name}
        response = self.session.put(
            f"{self.api_url}/name", verify=False, json=data, timeout=timeout
        )
        return response.status_code == 204

    def set_hostname(self, hostname: str, timeout: int = None) -> bool:
        data = {"hostname": hostname}
        response = self.session.put(
            f"{self.api_url}/server/hostname-for-access-keys",
            verify=False,
            json=data,
            timeout=timeout,
        )
        return response.status_code == 204

    def get_metrics_status(self, timeout: int = None) -> bool:
        response = self.session.get(
            f"{self.api_url}/metrics/enabled", verify=False, timeout=timeout
        )
        return response.json().get("metricsEnabled")

    def set_metrics_status(self, status: bool, timeout: int = None) -> bool:
        data = {"metricsEnabled": status}
        response = self.session.put(
            f"{self.api_url}/metrics/enabled", verify=False, json=data, timeout=timeout
        )
        return response.status_code == 204

    def set_port_new_for_access_keys(self, port: int, timeout: int = None) -> bool:
        data = {"port": port}
        response = self.session.put(
            f"{self.api_url}/server/port-for-new-access-keys",
            verify=False,
            json=data,
            timeout=timeout,
        )
        if response.status_code == 400:
            raise OutlineServerErrorException(
                "Invalid port parameter. Must be integer from 1 to 65535."
            )
        elif response.status_code == 409:
            raise OutlineServerErrorException(
                "The requested port is already in use."
            )
        return response.status_code == 204

    def set_data_limit_for_all_keys(
        self, limit_bytes: int, timeout: int = None
    ) -> bool:
        data = {"limit": {"bytes": limit_bytes}}
        response = self.session.put(
            f"{self.api_url}/server/access-key-data-limit",
            verify=False,
            json=data,
            timeout=timeout,
        )
        return response.status_code == 204

    def delete_data_limit_for_all_keys(self, timeout: int = None) -> bool:
        response = self.session.delete(
            f"{self.api_url}/server/access-key-data-limit",
            verify=False,
            timeout=timeout,
        )
        return response.status_code == 204

try:
    outline_vpn = OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)
except OutlineLibraryException as e:
    outline_vpn = None



def create_outline_access_key(name: str) -> str:

    if outline_vpn is None:
        print("OutlineVPN is not initialized")
        return ""
    try:
        key = outline_vpn.create_key(name=name)
        return key.access_url
    except OutlineServerErrorException as e:
        print(f"Error with creating an Outline key: {e}")
        return ""

def delete_outline_access_key(access_key_id: str) -> bool:

    if outline_vpn is None:
        print("OutlineVPN is not initialized")
        return False
    try:
        success = outline_vpn.delete_key(access_key_id)
        return success
    except OutlineServerErrorException as e:
        print(f"Error with deleting an Outline key: {e}")
        return False

def get_outline_access_keys() -> typing.List[OutlineKey]:

    global outline_vpn
    load_dotenv(dotenv_path="../.env")
    API_URL, CERT_SHA256 = parse_env_json("Json")
    try:
        outline_vpn = OutlineVPN(api_url=API_URL, cert_sha256=CERT_SHA256)
    except OutlineLibraryException as e:
        print(f"OutlineVPN is not initialized: {e}")
        return []

    if outline_vpn is None:
        print("OutlineVPN is not initialized")
        return []
    try:
        return outline_vpn.get_keys()
    except OutlineServerErrorException as e:
        print(f"Error with getting Outline keys: {e}")
        return []

def rename_outline_access_key(access_key_id: str, name: str) -> bool:

    if outline_vpn is None:
        print("OutlineVPN is not initialized")
        return False
    try:
        success = outline_vpn.rename_key(access_key_id, name)
        return success
    except OutlineServerErrorException as e:
        print(f"Error with renaming a key: {e}")
        return False

def extract_access_key_id(access_url: str) -> str:
    parsed_url = urllib.parse.urlparse(access_url)
    fragment = parsed_url.fragment

    if not fragment:
        return ""

    keys = get_outline_access_keys()
    for key in keys:
        if key.name == fragment:
            return key.key_id
    return ""