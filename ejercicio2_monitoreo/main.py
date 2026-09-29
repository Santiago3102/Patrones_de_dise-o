from infrastructure.adapters import LegacyAPIAdapter, ModernAPIAdapter
from infrastructure.external_apis import LegacyMonitoringAPI, ModernMonitoringAPI
from infrastructure.alert_channels import EmailAlert, SlackAlert, SMSAlert
from usecase.monitoring_facade import MonitoringFacade
from domain.config import MonitoringConfig


def main():
    ops = MonitoringFacade()
    ops.add_alert_channel(EmailAlert())
    ops.add_alert_channel(SlackAlert())

    ops.register_service("pagos-api", LegacyAPIAdapter(LegacyMonitoringAPI()))
    ops.register_service("antifraude", ModernAPIAdapter(ModernMonitoringAPI()))

    print("== Ciclo 1 (umbrales por defecto: cpu 80, memoria 85) ==")
    ops.run_cycle()

    print("\n== Se agrega SMS en caliente y se baja el umbral de CPU a 50 ==")
    ops.add_alert_channel(SMSAlert())
    ops.set_threshold("cpu", 50)
    ops.run_cycle()

    print("\nSingleton:", MonitoringConfig() is MonitoringConfig())


if __name__ == "__main__":
    main()
