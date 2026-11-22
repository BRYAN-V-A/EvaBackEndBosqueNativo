"""Entidad Cabana (tabla `cabanas`). Dataclass puro: no importa nada de Django.

El dinero se maneja con Decimal, nunca con float."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Cabana:
    codigo: str               # codigo interno unico (ej. CAB-01)
    nombre: str
    capacidad: int            # maximo de personas
    valor_noche: Decimal      # dinero: siempre Decimal
    activa: bool = True
    id: Optional[int] = None

    def admite(self, n_personas: int) -> bool:
        """Regla R2: el numero de personas no supera la capacidad de la cabana."""
        return 0 < n_personas <= self.capacidad

    def costo_estadia(self, noches: int) -> Decimal:
        """Parte de la regla R3: noches x valor_noche (los servicios se suman aparte)."""
        return self.valor_noche * noches
