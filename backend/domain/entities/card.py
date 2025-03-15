from dataclasses import dataclass
from uuid import UUID

from backend.domain.vo.requisites import CardRequisites


@dataclass
class Card:
    id: UUID
    number: CardRequisites
    user_id: int
    is_deleted: bool
