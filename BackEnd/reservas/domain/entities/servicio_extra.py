"""Entidad ServicioExtra (tabla `servicios_extra`): un servicio adicional que se
puede contratar en una reserva (tinaja, lena, desayuno...). Dataclass PURO."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class ServicioExtra:
    nombre: str
    precio: Decimal            # dinero: siempre Decimal
    id: Optional[int] = None

    def subtotal(self, cantidad: int) -> Decimal:
        """Cuanto cuesta contratar este servicio `cantidad` veces."""
        return self.precio * cantidad
