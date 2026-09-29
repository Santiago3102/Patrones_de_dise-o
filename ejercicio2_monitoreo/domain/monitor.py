from domain.alerts import Alert, AlertObserver
from domain.config import MonitoringConfig
from domain.metrics import MetricsProvider


class ServiceMonitor:
    """Subject del Observer: revisa un servicio y notifica si supera umbrales."""

    def __init__(self, name: str, provider: MetricsProvider):
        self.name = name
        self._provider = provider
        self._observers: list[AlertObserver] = []

    def attach(self, observer: AlertObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AlertObserver):
        self._observers.remove(observer)

    def check(self) -> list[Alert]:
        config = MonitoringConfig()
        alerts = []
        for metric, value in self._provider.get_metrics().items():
            threshold = config.get_threshold(metric)
            if threshold is not None and value > threshold:
                alert = Alert(self.name, metric, value, threshold)
                alerts.append(alert)
                for obs in self._observers:
                    obs.update(alert)
        return alerts
