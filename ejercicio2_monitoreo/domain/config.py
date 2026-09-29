import threading


class MonitoringConfig:
    """Singleton thread-safe: una única fuente de verdad para umbrales."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:                      # double-checked locking
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._thresholds = {"cpu": 80.0, "memory": 85.0}
                    inst._interval_seconds = 30
                    cls._instance = inst
        return cls._instance

    def get_threshold(self, metric):
        return self._thresholds.get(metric)

    def set_threshold(self, metric, value):
        with self._lock:
            self._thresholds[metric] = float(value)

    @property
    def interval_seconds(self):
        return self._interval_seconds
