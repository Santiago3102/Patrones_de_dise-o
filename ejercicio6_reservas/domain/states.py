from abc import ABC


class InvalidOperationError(Exception):
    pass


class ReservationState(ABC):
    """State: cada estado decide qué operaciones son válidas.
    Por defecto TODO está prohibido; cada estado habilita lo suyo."""
    name = "BASE"

    def _deny(self, op):
        raise InvalidOperationError(
            f"No se puede '{op}' una reserva en estado {self.name}")

    def confirm(self, r):            self._deny("confirmar")
    def cancel(self, r):             self._deny("cancelar")
    def check_in(self, r):           self._deny("hacer check-in de")
    def board(self, r):              self._deny("abordar")
    def add_service(self, r, n, p):  self._deny("modificar")
    def upgrade(self, r, pricing):   self._deny("hacer upgrade de")

    def amount_due(self, r):
        return r.total_price()


class PendingState(ReservationState):
    name = "PENDIENTE"

    def confirm(self, r):            r._set_state(ConfirmedState())
    def cancel(self, r):             r._set_state(CancelledState())
    def add_service(self, r, n, p):  r._services.append((n, p))
    def upgrade(self, r, pricing):   r._apply_upgrade(pricing)


class ConfirmedState(ReservationState):
    name = "CONFIRMADA"

    def cancel(self, r):             r._set_state(CancelledState())
    def check_in(self, r):           r._set_state(CheckedInState())
    def upgrade(self, r, pricing):   r._apply_upgrade(pricing)


class CheckedInState(ReservationState):
    name = "CHECK-IN"

    def board(self, r):              r._set_state(BoardedState())


class BoardedState(ReservationState):
    name = "ABORDADA"


class CancelledState(ReservationState):
    name = "CANCELADA"

    def amount_due(self, r):         # regla: canceladas no generan cargos
        return 0.0
