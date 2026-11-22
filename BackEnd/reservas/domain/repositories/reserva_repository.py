"""Puerto de salida para Reserva (incluye sus detalles). DetalleServicio no tiene
puerto propio: sus lineas se guardan y se leen siempre junto con su reserva."""

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from reservas.domain.entities import Reserva


class ReservaRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Reserva]:
        ...

    @abstractmethod
    def obtener_por_id(self, reserva_id: int) -> Optional[Reserva]:
        ...

    @abstractmethod
    def hay_cruce(self, cabana_id: int, llegada: date, salida: date,
                  excluir_id: Optional[int] = None) -> bool:
        """Regla R1: la cabana ya tiene una reserva NO cancelada que se cruza con
        esas fechas. excluir_id: al editar, no contar a la propia reserva."""
        ...

    @abstractmethod
    def registrar(self, reserva: Reserva) -> Reserva:
        """Guarda la reserva con sus detalles, TODO o NADA: si falla un detalle,
        no queda nada guardado."""
        ...

    @abstractmethod
    def cambiar_estado(self, reserva: Reserva, nuevo_estado: str) -> Reserva:
        ...

    @abstractmethod
    def eliminar(self, reserva_id: int) -> bool:
        """Borra la reserva; sus detalles se borran en cascada."""
        ...
