import time
from domain.alerts import AlertObserver
from domain.metrics import MetricsProvider
from domain.monitor import ServiceMonitor
from domain.config import MonitoringConfig


class MonitoringFacade:
    """Punto único de entrada para el equipo de operaciones."""

    def __init__(self):
        self._monitors: dict[str, ServiceMonitor] = {}
        self._channels: list[AlertObserver] = []

    def add_alert_channel(self, channel: AlertObserver):
        self._channels.append(channel)
        for m in self._monitors.values():
            m.attach(channel)

    def register_service(self, name: str, provider: MetricsProvider):
        monitor = ServiceMonitor(name, provider)
        for ch in self._channels:
            monitor.attach(ch)
        self._monitors[name] = monitor

    def set_threshold(self, metric: str, value: float):
        MonitoringConfig().set_threshold(metric, value)

    def run_cycle(self):
        alerts = []
        for monitor in self._monitors.values():
            alerts.extend(monitor.check())
        return alerts

    def start(self, cycles: int = 1):
        """Monitoreo periódico (cycles finito para poder demostrarlo)."""
        for i in range(cycles):
            self.run_cycle()
            if i < cycles - 1:
                time.sleep(MonitoringConfig().interval_seconds)
