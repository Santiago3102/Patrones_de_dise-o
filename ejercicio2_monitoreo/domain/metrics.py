from abc import ABC, abstractmethod


class MetricsProvider(ABC):
    """Interfaz destino (Target del Adapter). El núcleo solo conoce esto."""

    @abstractmethod
    def get_cpu_usage(self) -> float: ...

    @abstractmethod
    def get_memory_usage(self) -> float: ...

    def get_metrics(self) -> dict:
        """Métricas normalizadas (0-100). Para una métrica nueva: agregar
        un método abstracto y una clave aquí + un umbral en la config."""
        return {"cpu": self.get_cpu_usage(), "memory": self.get_memory_usage()}
