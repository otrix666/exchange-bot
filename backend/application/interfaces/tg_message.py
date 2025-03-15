from typing import Protocol


class PhotoSize(Protocol):
    file_id: str


class Animation(Protocol):
    file_id: str


class Video(Protocol):
    file_id: str


class Document(Protocol):
    file_id: str


class Message(Protocol):
    message_id: int
    content_type: str
    photo: list[PhotoSize] | None
    animation: Animation | None
    video: Video | None
    document: Document | None
