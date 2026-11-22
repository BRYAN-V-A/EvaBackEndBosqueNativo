"""Entidad DetalleServicio (tabla `detalle_servicio`): un servicio extra contratado
dentro de una reserva.

No tiene id propio: se identifica por la pareja (reserva, servicio). Por eso no
tiene repositorio propio: se guarda y se lee SIEMPRE junto con su Reserva (la
Reserva es la "raiz" que agrupa a sus detalles)."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class DetalleServicio:
    servicio_id: int
    cantidad: int
    precio_unitario: Decimal
    reserva_id: Optional[int] = None

    @property
    def subtotal(self) -> Decimal:
        """Misma formula que la columna calculada (virtual) de Oracle."""
        return self.cantidad * self.precio_unitario
