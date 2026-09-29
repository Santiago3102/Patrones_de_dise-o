from abc import ABC, abstractmethod


class ReservationObserver(ABC):
    @abstractmethod
    def update(self, event: str, reservation) -> None: ...
