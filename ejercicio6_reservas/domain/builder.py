from datetime import date
from domain.entities import Flight, Passenger
from domain.pricing import PricingStrategy, EconomyPricing
from domain.reservation import Reservation


class ReservationBuilder:
    """Builder fluido: valida que el objeto quede consistente en build()."""

    def __init__(self):
        self._passenger = None
        self._flight = None
        self._base_price = None
        self._pricing: PricingStrategy = EconomyPricing()   # valor por defecto
        self._seat = None
        self._services = []
        self._preferences = {}
        self._purchase_date = date.today()

    def for_passenger(self, p: Passenger):     self._passenger = p; return self
    def on_flight(self, f: Flight):            self._flight = f; return self
    def with_base_price(self, price: float):   self._base_price = price; return self
    def with_pricing(self, s: PricingStrategy):self._pricing = s; return self
    def with_seat(self, seat: str):            self._seat = seat; return self
    def add_service(self, name, price):        self._services.append((name, price)); return self
    def with_preference(self, key, value):     self._preferences[key] = value; return self
    def purchased_on(self, d: date):           self._purchase_date = d; return self

    def build(self) -> Reservation:
        if not self._passenger or not self._flight:
            raise ValueError("Una reserva requiere pasajero y vuelo")
        if self._base_price is None or self._base_price <= 0:
            raise ValueError("Precio base inválido")
        if self._purchase_date >= self._flight.departure:
            raise ValueError("La compra debe ser anterior a la salida")
        return Reservation(self._passenger, self._flight, self._base_price,
                           self._pricing, self._seat, self._services,
                           self._preferences, self._purchase_date)
