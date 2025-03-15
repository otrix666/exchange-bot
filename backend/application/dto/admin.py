from dataclasses import dataclass
from datetime import datetime

from backend.application.dto.statistic import ExchangeStat


@dataclass(slots=True)
class BasicUser:
    id: int
    username: str
    full_name: str
    is_banned: bool
    created_at: datetime


@dataclass(slots=True)
class UserProfile:
    user: BasicUser
    statistic: ExchangeStat
