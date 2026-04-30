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

class FileChannel(NotificationChannel):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def is_available(self) -> bool:
        directory = os.path.dirname(self.file_path) or "."

        if os.path.exists(self.file_path):
            return os.access(self.file_path, os.W_OK)

        return os.path.isdir(directory) and os.access(directory, os.W_OK)

    def get_channel_name(self) -> str:
        return f"file:{self.file_path}"

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError(
                f"Archivo no disponible: {self.file_path}"
            )

        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            raise DeliveryError(f"Error escribiendo archivo: {e}")
