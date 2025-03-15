from dataclasses import dataclass


@dataclass(slots=True)
class Cheque:
    id: int | None
    url: str
