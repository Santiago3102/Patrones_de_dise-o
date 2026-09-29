from datetime import date
from domain.entities import Flight, Passenger
from domain.pricing import PricingStrategy
from domain.states import PendingState, ReservationState
from interfaces.observers import ReservationObserver


class Reservation:
    """Contexto del State + Subject del Observer + Context del Strategy."""

    def __init__(self, passenger: Passenger, flight: Flight, base_price: float,
                 pricing: PricingStrategy, seat: str, services: list,
                 preferences: dict, purchase_date: date):
        self.passenger = passenger
        self.flight = flight
        self.base_price = base_price
        self.seat = seat
        self.preferences = preferences
        self.purchase_date = purchase_date
        self._pricing = pricing
        self._services = list(services)          # [(nombre, precio)]
        self._state: ReservationState = PendingState()
        self._observers: list[ReservationObserver] = []

    # ---- Observer ----
    def attach(self, o: ReservationObserver):   self._observers.append(o)
    def detach(self, o: ReservationObserver):   self._observers.remove(o)

    def _notify(self, event: str):
        for o in self._observers:
            o.update(event, self)

    # ---- consultas ----
    @property
    def state_name(self):    return self._state.name
    @property
    def pricing_name(self):  return self._pricing.name
    @property
    def services(self):      return list(self._services)

    def total_price(self) -> float:
        days = (self.flight.departure - self.purchase_date).days
        services_total = sum(p for _, p in self._services)
        return self._pricing.calculate(self.base_price, services_total, days)

    def amount_due(self) -> float:
        return self._state.amount_due(self)

    # ---- operaciones: se delegan al estado ----
    def confirm(self):   self._state.confirm(self)
    def cancel(self):    self._state.cancel(self)
    def check_in(self):  self._state.check_in(self)
    def board(self):     self._state.board(self)

    def add_service(self, name: str, price: float):
        self._state.add_service(self, name, price)
        self._notify(f"SERVICIO_AGREGADO:{name}")

    def upgrade(self, new_pricing: PricingStrategy) -> float:
        before = self.total_price()
        self._state.upgrade(self, new_pricing)
        return round(self.total_price() - before, 2)   # diferencia a cobrar

    # ---- uso interno de los estados ----
    def _set_state(self, state: ReservationState):
        old = self._state.name
        self._state = state
        self._notify(f"ESTADO:{old}->{state.name}")

    def _apply_upgrade(self, pricing: PricingStrategy):
        old = self._pricing.name
        self._pricing = pricing
        self._notify(f"UPGRADE:{old}->{pricing.name}")
