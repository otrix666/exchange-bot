from dataclasses import dataclass


@dataclass(slots=True)
class PrivateKeyHex:
    private_key: str


@dataclass(slots=True)
class Wallet:
    id: int | None
    private_key_hex: str
    is_deleted: bool
