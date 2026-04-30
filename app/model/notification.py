import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable

from app.services.util import generate_unique_id
from abc import ABC, abstractmethod
import os


class NotificationError(Exception):
    pass


class ChannelUnavailableError(NotificationError):
    pass


class DeliveryError(NotificationError):
    pass

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class ConsoleChannel(NotificationChannel):

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError("Console no disponible")

        try:
            print(message)
        except Exception as e:
            raise DeliveryError(f"Error al imprimir: {e}")

    def get_channel_name(self) -> str:
        return "console"

    def is_available(self) -> bool:
        return True