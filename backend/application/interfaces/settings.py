from abc import abstractmethod
from typing import Protocol

from backend.domain.entities.settings import Settings


class SettingsReader(Protocol):
    @abstractmethod
    def read(self) -> Settings:
        raise NotImplementedError


class SettingsWriter(Protocol):
    @abstractmethod
    def write(self, settings: Settings):
        raise NotImplementedError
