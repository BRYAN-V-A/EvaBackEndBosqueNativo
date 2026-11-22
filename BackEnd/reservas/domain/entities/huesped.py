"""Entidad Huesped (tabla `huespedes`). Dataclass puro: no importa nada de Django."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Huesped:
    documento: str            # rut (chilenos) o pasaporte (extranjeros); es unico
    nombre: str
    pais: str
    email: Optional[str] = None
    id: Optional[int] = None

    def es_chileno(self) -> bool:
        """Regla de negocio pura: no depende de Django ni de la BD."""
        return self.pais.strip().lower() == "chile"
