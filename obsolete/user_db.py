from dataclasses import dataclass, field
from enum import Enum, verify, UNIQUE
from user_settings import UserSettings
from user_state import UserState
from typing import Callable


@dataclass
class User:
    """User info in db"""
    settings: UserSettings
    state: UserState


class UserDB:
    class UserNotFoundError(Exception):
        def __init__(self, user_id):
            super().__init__(f"User {user_id} is not in database")

    async def get_user_settings(self, user_id: str) -> dict[str, str]:
        """Fetch plain dict of user settings. Dict format: {'path.to.option': 'value'}"""
        raise NotImplementedError()

    async def set_user_settings(self, user_id: str) -> dict[str, str]:
        """Fetch plain dict of user settings. Dict format: {'path.to.option': 'value'}"""
        raise NotImplementedError()

    async def get_user_state(self, user_id: str) -> UserState:
        """Fetch current user state and """
        raise NotImplementedError()

    async def set_user_state(self, user_id: str, user_state: UserState):
        """Set current user state"""
        raise NotImplementedError()

    async def add_user(self, user_id: str) -> User:
        """Add user to database and return user record"""
        raise NotImplementedError()

    async def remove_user(self, user_id: str):
        """Remove user records from database"""
        raise NotImplementedError()


class MemoryUserDBImpl(UserDB):
    def __init__(self):
        self._user_data: dict[str, User] = {}

    @staticmethod
    def _check_user_in_db(condition: bool = True):
        def wrapper(func: Callable):
            def checker(self, user_id, *args, **kwargs):
                if (user_id in self._user_data) == condition:
                    raise UserDB.UserNotFoundError(user_id)
                return func(self, user_id * args, **kwargs)

            return checker

        return wrapper

    @_check_user_in_db
    async def get_user_settings(self, user_id: str) -> UserSettings:
        return self._user_data[user_id].settings

    @_check_user_in_db
    async def set_user_settings(self, user_id: str, user_settings: UserState):
        self._user_data[user_id].settings = user_settings

    @_check_user_in_db
    async def get_user_state(self, user_id: str) -> UserState:
        return self._user_data[user_id].state

    @_check_user_in_db
    async def set_user_state(self, user_id: str, user_state: UserState):
        self._user_data[user_id].state = user_state

    @_check_user_in_db(False)
    async def add_user(self, user_id: str) -> User:
        return self._user_data.setdefault(user_id, User(UserSettings(), UserState.DEFAULT()))

    @_check_user_in_db
    async def remove_user(self, user_id: str):
        del self._user_data[user_id]
