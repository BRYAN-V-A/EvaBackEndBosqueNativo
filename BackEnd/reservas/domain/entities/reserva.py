"""Entidad Reserva (tabla `reservas`), con sus lineas de DetalleServicio.

Las relaciones se guardan como ids (huesped_id, cabana_id), no como objetos.
Aca viven las reglas que dependen SOLO de los datos de la propia reserva."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from .detalle_servicio import DetalleServicio

ESTADOS_RESERVA = ("pendiente", "confirmada", "finalizada", "cancelada")

NOCHES_MINIMAS = 2   # regla R3

# Reglas de negocio: a que estado puede pasar una reserva desde cada estado
TRANSICIONES = {
    "pendiente": ("confirmada", "cancelada"),
    "confirmada": ("finalizada", "cancelada"),
    "finalizada": (),
    "cancelada": (),
}


@dataclass
class Reserva:
    huesped_id: int
    cabana_id: int
    fecha_llegada: date
    fecha_salida: date
    n_personas: int
    detalles: List[DetalleServicio] = field(default_factory=list)
    estado: str = "pendiente"
    total: Decimal = Decimal("0")
    id: Optional[int] = None

    def noches(self) -> int:
        return (self.fecha_salida - self.fecha_llegada).days

    def cumple_estadia_minima(self) -> bool:
        """Regla R3: minimo 2 noches."""
        return self.noches() >= NOCHES_MINIMAS

    def total_servicios(self) -> Decimal:
        return sum((d.subtotal for d in self.detalles), Decimal("0"))

    def calcular_total(self, valor_noche: Decimal) -> Decimal:
        """Regla R3: total = noches x valor_noche + servicios."""
        return self.noches() * valor_noche + self.total_servicios()

    def se_cruza_con(self, llegada: date, salida: date) -> bool:
        """Regla R1: dos estadias se cruzan si cada una empieza antes
        de que termine la otra. Si una sale el mismo dia que la otra llega, NO se cruzan."""
        return self.fecha_llegada < salida and llegada < self.fecha_salida

    def puede_pasar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in TRANSICIONES[self.estado]