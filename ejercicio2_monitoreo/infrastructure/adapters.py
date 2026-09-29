from domain.metrics import MetricsProvider
from infrastructure.external_apis import LegacyMonitoringAPI, ModernMonitoringAPI


class LegacyAPIAdapter(MetricsProvider):
    def __init__(self, api: LegacyMonitoringAPI):
        self._api = api

    def get_cpu_usage(self):
        return float(self._api.fetch()["cpu_usage_percent"])

    def get_memory_usage(self):
        return float(self._api.fetch()["mem_used_pct"])


class ModernAPIAdapter(MetricsProvider):
    def __init__(self, api: ModernMonitoringAPI):
        self._api = api

    def get_cpu_usage(self):
        return self._api.query()["metrics"]["cpu"]["utilization"] * 100

    def get_memory_usage(self):
        return self._api.query()["metrics"]["memory"]["utilization"] * 100
