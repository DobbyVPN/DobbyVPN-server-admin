from typing import List

class Action:
	@property
	def description(self) -> str:
		raise NotImplementedError
	

	def execute(self):
		raise NotImplementedError


class ActionContext:
	@property
	def actions(self):
		raise NotImplementedError
