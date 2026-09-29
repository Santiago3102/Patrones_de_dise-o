from datetime import date
from domain.builder import ReservationBuilder
from domain.entities import Flight, Passenger
from domain.pricing import PremiumPricing, FirstClassPricing
from domain.states import InvalidOperationError
from infrastructure.notifiers import EmailNotifier, SMSNotifier, AppNotifier


def main():
    flight = Flight("AV9302", "PEI", "BOG", date(2026, 12, 20))
    pax = Passenger("Santiago", "santiago@mail.com", "+57 300 000 0000")

    r = (ReservationBuilder()
         .for_passenger(pax).on_flight(flight)
         .with_base_price(300_000).with_seat("12A")
         .add_service("Maleta 23kg", 60_000)
         .with_preference("comida", "vegetariana")
         .purchased_on(date(2026, 9, 28))
         .build())
    for n in (EmailNotifier(), SMSNotifier(), AppNotifier()):
        r.attach(n)

    print(f"Estado: {r.state_name} | Tarifa: {r.pricing_name} | Total: {r.total_price():,.0f}")

    print("\n-- Agregar servicio (PENDIENTE: permitido) --")
    r.add_service("Selección de asiento", 20_000)

    print("\n-- Confirmar --")
    r.confirm()

    print("\n-- Modificar en CONFIRMADA (debe fallar) --")
    try:
        r.add_service("Wifi", 15_000)
    except InvalidOperationError as e:
        print("  Error:", e)

    print("\n-- Upgrade a Premium --")
    diff = r.upgrade(PremiumPricing())
    print(f"  Diferencia a cobrar: {diff:,.0f} | Nuevo total: {r.total_price():,.0f}")

    print("\n-- Check-in y abordaje --")
    r.check_in(); r.board()

    print("\n-- Cancelar una reserva ya abordada (debe fallar) --")
    try:
        r.cancel()
    except InvalidOperationError as e:
        print("  Error:", e)

    print("\n== Reserva 2: cancelación sin cargos ==")
    r2 = (ReservationBuilder().for_passenger(pax).on_flight(flight)
          .with_base_price(500_000).with_pricing(FirstClassPricing())
          .purchased_on(date(2026, 9, 28)).build())
    r2.attach(EmailNotifier())
    print(f"Total: {r2.total_price():,.0f}")
    r2.cancel()
    print(f"Estado: {r2.state_name} | Cargo tras cancelar: {r2.amount_due():,.0f}")


if __name__ == "__main__":
    main()
