import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from typing import List
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

class MockChannel(NotificationChannel):

    def send(self, message: str) -> None:
        raise ChannelUnavailableError("Mock no disponible")

    def get_channel_name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return False

@dataclass
class DeliveryReport:
    channel_name: str
    total_attempted: int
    total_delivered: int
    messages: list[str] = field(default_factory=list)
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def success_rate(self) -> float:
        if self.total_attempted == 0:
            return 0.0
        return self.total_delivered / self.total_attempted

    def is_empty(self) -> bool:
        return self.total_delivered == 0

    def __str__(self) -> str:
        return (
            f"DeliveryReport(channel={self.channel_name}, "
            f"attempted={self.total_attempted}, "
            f"delivered={self.total_delivered}, "
            f"success_rate={self.success_rate():.2f}, "
            f"report_id={self.report_id})"
        )

class NotificationService:

    def __init__(self, channel: NotificationChannel):
        self._channel = channel
        self._history: List[str] = []

    def send_notification(self, message: str) -> None:
        if not self._channel.is_available():
            raise ChannelUnavailableError(
                f"Channel not available: {self._channel.get_channel_name()}"
            )

        self._channel.send(message)
        self._history.append(message)

    def send_bulk(self, messages: List[str]) -> int:
        success_count = 0

        for msg in messages:
            try:
                self.send_notification(msg)
                success_count += 1
            except NotificationError:
                continue

        return success_count

    def get_history(self) -> List[str]:
        return list(self._history)

    # 🔹 Integración con DeliveryReport
    def generate_report(self, attempted: List[str]) -> "DeliveryReport":
        return DeliveryReport(
            channel_name=self._channel.get_channel_name(),
            attempted=len(attempted),
            delivered=len(self._history),
            delivered_messages=self.get_history()
        )

