from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Alert:
    service: str
    metric: str
    value: float
    threshold: float


class AlertObserver(ABC):
    """Observer: cada canal de alerta implementa update()."""

    @abstractmethod
    def update(self, alert: Alert) -> None: ...
