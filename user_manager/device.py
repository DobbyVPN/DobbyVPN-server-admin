from typing import List

class Device:
	def __init__(self, dtype: str, keys: List[str]):
		self._dtype = dtype
		self._keys = keys

	@property
	def dtype(self) -> str:
		return self._dtype

	@property
	def keys(self) -> List[str]:
		return self._keys
