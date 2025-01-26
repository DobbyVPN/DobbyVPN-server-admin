from actions.root_action import *
from actions.user_manager import UserManager


user_manager = UserManager()
context = RootContext()
context.add_action(MakeUserAction(user_manager, context))
context.add_action(ListUsersAction(user_manager, context))
context.add_action(DelUserAction(user_manager, context))


if __name__ == "__main__":
	while True:
		context_actions = context.actions
		context_actions_indices = range(len(context_actions))

		for index, action in zip(context_actions_indices, context_actions):
			print(f"[{index + 1}] {action.description}")

		user_chose = input("Select action or write down 'q' to exit: ")

		if user_chose == 'q':
			break
		else:
			action_index = int(user_chose) - 1
			user_action = context_actions[action_index]
			context = user_action.execute()
