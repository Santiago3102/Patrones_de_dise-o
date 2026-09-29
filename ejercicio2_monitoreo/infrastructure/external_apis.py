"""APIs externas simuladas. NO se pueden modificar (son de terceros)."""


class LegacyMonitoringAPI:
    def fetch(self) -> dict:
        return {"cpu_usage_percent": 85, "mem_used_pct": 60}


class ModernMonitoringAPI:
    def query(self) -> dict:
        return {"metrics": {"cpu": {"utilization": 0.55},
                            "memory": {"utilization": 0.91}}}
