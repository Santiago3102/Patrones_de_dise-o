from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """Strategy: cada tarifa es un algoritmo intercambiable."""
    name = "BASE"

    @abstractmethod
    def calculate(self, base_price: float, services_total: float,
                  days_before_departure: int) -> float: ...


class EconomyPricing(PricingStrategy):
    name = "ECONOMICA"

    def calculate(self, base_price, services_total, days_before_departure):
        total = base_price + services_total
        if days_before_departure < 7:          # compra de último minuto
            total *= 1.15
        return round(total, 2)


class PremiumPricing(PricingStrategy):
    name = "PREMIUM"

    def calculate(self, base_price, services_total, days_before_departure):
        return round(base_price * 1.6 + services_total, 2)


class FirstClassPricing(PricingStrategy):
    name = "PRIMERA"

    def calculate(self, base_price, services_total, days_before_departure):
        # servicios con 50% de descuento (lounge incluido)
        return round(base_price * 2.5 + services_total * 0.5, 2)
