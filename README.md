# Taller II: Patrones de Diseño (IS924)

Implementaciones en Python de soluciones empresariales que integran varios patrones de diseño sobre un mismo problema. Cada ejercicio está organizado en capas y es extensible sin modificar el código existente (principio Open/Closed).

| Ejercicio | Problema | Patrones |
|---|---|---|
| `ejercicio2_monitoreo` | Monitoreo de microservicios con alertas multicanal | Singleton, Observer, Adapter, Facade |
| `ejercicio6_reservas` | Reservas de aerolínea con ciclo de vida y precios dinámicos | Builder, Strategy, State, Observer |

## Requisitos

- Python 3.9 o superior
- Sin dependencias externas (solo librería estándar)

## Ejecución

Cada ejercicio se ejecuta desde su propia carpeta:

```bash
cd ejercicio2_monitoreo
python main.py
```

```bash
cd ejercicio6_reservas
python main.py
```

En macOS o Linux usa `python3` si `python` no está disponible.

> Ejecuta siempre desde dentro de la carpeta del ejercicio. Si aparece `ModuleNotFoundError: No module named 'domain'`, estás en otra ruta.

## Arquitectura

Ambos ejercicios siguen la misma organización por capas, con la dependencia apuntando siempre hacia el dominio:

| Carpeta | Contenido |
|---|---|
| `domain/` | Entidades, reglas del negocio y abstracciones del núcleo. No importa nada de infraestructura. |
| `interfaces/` | Contratos que el dominio necesita (cuando no viven en `domain/`). |
| `infrastructure/` | Implementaciones concretas: canales de notificación, adapters, APIs externas simuladas. |
| `usecase/` | Orquestación de alto nivel (Facade). |
| `main.py` | Punto de entrada: arma las piezas y ejecuta una demostración. |

---

## Ejercicio 2: Sistema de Monitoreo de Microservicios

Un monitor por servicio consulta métricas (a través de APIs externas con formatos distintos), las compara con umbrales centralizados y notifica a los canales suscritos cuando se superan.

```
ejercicio2_monitoreo/
├── main.py
├── domain/
│   ├── config.py            # MonitoringConfig (Singleton)
│   ├── metrics.py           # MetricsProvider (interfaz)
│   ├── alerts.py            # Alert + AlertObserver (interfaz)
│   └── monitor.py           # ServiceMonitor (Subject)
├── infrastructure/
│   ├── external_apis.py     # APIs de terceros simuladas
│   ├── adapters.py          # LegacyAPIAdapter, ModernAPIAdapter
│   └── alert_channels.py    # EmailAlert, SlackAlert, SMSAlert
└── usecase/
    └── monitoring_facade.py # MonitoringFacade
```

| Patrón | Clase(s) | Rol |
|---|---|---|
| Singleton | `MonitoringConfig` | Única fuente de umbrales, thread-safe con `Lock` |
| Observer | `ServiceMonitor`, `AlertObserver`, `EmailAlert`, `SlackAlert`, `SMSAlert` | El monitor notifica alertas sin conocer los canales |
| Adapter | `LegacyAPIAdapter`, `ModernAPIAdapter` | Traducen cada API externa a `MetricsProvider` |
| Facade | `MonitoringFacade` | Punto único: `register_service()`, `add_alert_channel()`, `set_threshold()`, `run_cycle()` |

Ejemplo de salida:

```
== Ciclo 1 (umbrales por defecto: cpu 80, memoria 85) ==
  [EMAIL] pagos-api: cpu = 85% (umbral 80%)
  [SLACK] pagos-api: cpu = 85% (umbral 80%)
  [EMAIL] antifraude: memory = 91% (umbral 85%)
  [SLACK] antifraude: memory = 91% (umbral 85%)
...
Singleton: True
```

**Cómo extenderlo**
- *Nuevo canal:* crear una clase que herede de `AlertObserver` y registrarla con `add_alert_channel()`.
- *Nueva API externa:* crear un adapter que implemente `MetricsProvider`.
- *Nueva métrica:* agregar el método en `MetricsProvider`, su clave en `get_metrics()` y un umbral con `set_threshold()`.

---

## Ejercicio 6: Sistema de Reservas para Aerolínea

Una reserva se construye paso a paso, calcula su precio según la tarifa, cambia de estado con reglas propias y notifica cada cambio.

```
ejercicio6_reservas/
├── main.py
├── domain/
│   ├── entities.py          # Passenger, Flight
│   ├── pricing.py           # PricingStrategy + Economy / Premium / FirstClass
│   ├── states.py            # ReservationState + 5 estados concretos
│   ├── reservation.py       # Reservation (contexto)
│   └── builder.py           # ReservationBuilder
├── interfaces/
│   └── observers.py         # ReservationObserver (contrato)
└── infrastructure/
    └── notifiers.py         # EmailNotifier, SMSNotifier, AppNotifier
```

| Patrón | Clase(s) | Rol |
|---|---|---|
| Builder | `ReservationBuilder` | Construcción fluida con validación en `build()` |
| Strategy | `EconomyPricing`, `PremiumPricing`, `FirstClassPricing` | Algoritmos de precio intercambiables (permiten el upgrade) |
| State | `PendingState`, `ConfirmedState`, `CheckedInState`, `BoardedState`, `CancelledState` | Cada estado define qué operaciones permite |
| Observer | `Reservation`, `ReservationObserver`, notificadores | Notificación de cada cambio por múltiples canales |

Flujo de estados:

```
Pendiente ──confirm()──► Confirmada ──check_in()──► Check-in ──board()──► Abordada
    │                        │
    └────── cancel() ────────┴──────► Cancelada (amount_due = 0)
```

Reglas de negocio implementadas:
- Solo se pueden agregar servicios en estado **pendiente**.
- El **upgrade** de tarifa solo es válido en estado pendiente o confirmada y devuelve la diferencia a cobrar.
- Una reserva **cancelada** no genera cargos.
- Cualquier operación no permitida por el estado lanza `InvalidOperationError`.

Ejemplo de salida:

```
Estado: PENDIENTE | Tarifa: ECONOMICA | Total: 360,000
-- Modificar en CONFIRMADA (debe fallar) --
  Error: No se puede 'modificar' una reserva en estado CONFIRMADA
-- Upgrade a Premium --
  UPGRADE:ECONOMICA->PREMIUM
  Diferencia a cobrar: 180,000 | Nuevo total: 560,000
```

Los errores mostrados en la demo son intencionales: comprueban que State bloquea operaciones inválidas.

**Cómo extenderlo**
- *Nueva tarifa:* crear una clase que herede de `PricingStrategy`.
- *Nuevo estado (ej. lista de espera):* crear una clase que herede de `ReservationState`; todo lo que no se habilite queda prohibido por defecto.
- *Nuevo canal:* crear una clase que herede de `ReservationObserver` y suscribirla con `attach()`.

---

## Autor

Santiago: Ingeniería de Software, Universidad Tecnológica de Pereira
Asignatura: Arquitectura Cliente-Servidor (IS924)
