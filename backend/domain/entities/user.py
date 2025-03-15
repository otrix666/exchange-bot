from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class User:
    id: int
    username: str | None
    full_name: str
    is_banned: bool
    created_at: datetime
