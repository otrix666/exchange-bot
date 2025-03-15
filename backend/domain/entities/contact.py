from dataclasses import dataclass


@dataclass
class Contact:
    id: int | None
    title: str
    url: str
