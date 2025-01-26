from typing import List
from actions.action import Action, ActionContext
from actions.user_manager import UserManager

class RootContext(ActionContext):
	def __init__(self):
		self._actions = []

	def add_action(self, action: Action):
		self._actions.append(action)

	@property
	def actions(self) -> List[Action]:
		return self._actions


class MakeUserAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Make new user"

	def execute(self) -> ActionContext:
		user_name = input("Put user name: ")
		new_user = self._user_manager.add_user(user_name)
		new_user.print_data()

		return self._root_context


class ListUsersAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "List all users"

	def execute(self) -> ActionContext:
		all_users = self._user_manager.users
		indicies = range(0, len(all_users))
		for index, user in zip(indicies, all_users):
			print(f"{index + 1}) {user.name}")

		return self._root_context


class DelUserAction(Action):
	def __init__(self, user_manager: UserManager, root_context: ActionContext):
		self._user_manager = user_manager
		self._root_context = root_context

	@property
	def description(self) -> str:
		return "Delete user"

	def execute(self) -> ActionContext:
		all_users = self._user_manager.users
		indicies = range(0, len(all_users))
		for index, user in zip(indicies, all_users):
			print(f"{index + 1}) {user.name}")

		user_chose = int(input("Enter user index: "))
		user_index = user_chose - 1
		removing_user = all_users[user_index]

		if input(f"Remove user #{user_chose} {removing_user.name} [y/N]? ") == 'y':
			self._user_manager.remove_user(user_index)

		return self._root_context
