import enum


class _UserStateBase:
    """Base class for all user state options"""
    pass


class _UserStateIdle(_UserStateBase):
    """Idle user state options"""
    pass


@enum.verify(enum.UNIQUE)
class UserState(enum.Enum):
    """Mapping from user state name to user state options class"""
    DEFAULT = _UserStateIdle
    IDLE = _UserStateIdle
