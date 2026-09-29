from interfaces.observers import ReservationObserver


class EmailNotifier(ReservationObserver):
    def update(self, event, r):
        print(f"  [EMAIL -> {r.passenger.email}] {event}")


class SMSNotifier(ReservationObserver):
    def update(self, event, r):
        print(f"  [SMS   -> {r.passenger.phone}] {event}")


class AppNotifier(ReservationObserver):
    def update(self, event, r):
        print(f"  [PUSH  -> app] {event} (vuelo {r.flight.code})")
