from actions import *
from user_manager import UserManager
from util import *


if __name__ == "__main__":
	user_manager = UserManager()
	context = RootContext()
	context.add_action(MakeUserAction(user_manager, context))
	context.add_action(ListKeysAction(user_manager, context))
	context.add_action(DelUserAction(user_manager, context))
	context.add_action(AddInterfaceAction(user_manager, context))
	context.add_action(ListInterfacesAction(user_manager, context))

	while True:
		for index, action in with_index(context.actions):
			print(f"[{index + 1}] {action.description}")

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
				user_action = context.actions[action_index]
			except Exception:
				print("Invalid input")
				continue

			try:
				context = user_action.execute()
			except Exception as ex:
				print(f"Exception during user action execute: {ex}")
