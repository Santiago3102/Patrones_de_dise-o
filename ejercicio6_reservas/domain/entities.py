from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Passenger:
    name: str
    email: str
    phone: str = ""


@dataclass(frozen=True)
class Flight:
    code: str
    origin: str
    destination: str
    departure: date
