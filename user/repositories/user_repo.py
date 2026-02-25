from abc import ABC, abstractmethod
from typing import Dict

from user.models.user import User

class UserAbstraction (ABC):
	@abstractmethod
	async def get_user (self, user_id: int) -> User:
		pass

	@abstractmethod
	async def create_user (self, user_email: str) -> User:
		pass

	@abstractmethod
	async def delete_user (self, user_id: int) -> Dict[str, int]:
		pass

	@abstractmethod
	async def update_user (self, user_id: int)-> User:
		pass
