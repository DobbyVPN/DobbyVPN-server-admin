from typing import List
from user_manager.user import User

class VpnInterface:
	def list_users(self) -> List[User]:
		raise NotImplementedError
	
	def add_user(self, user_name: str) -> User:
		raise NotImplementedError

	def remove_user(self, user_name: str):
		raise NotImplementedError

	def print_data(self):
		raise NotImplementedError
