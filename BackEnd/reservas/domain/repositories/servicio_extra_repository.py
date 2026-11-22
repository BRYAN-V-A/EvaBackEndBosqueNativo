"""Puerto de salida para ServicioExtra."""

from abc import ABC, abstractmethod
from typing import List, Optional
from reservas.domain.entities import ServicioExtra


class ServicioExtraRepository(ABC):

    @abstractmethod
    def listar(self) -> List[ServicioExtra]:
        ...

    @abstractmethod
    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioExtra]:
        ...

    @abstractmethod
    def existe_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        """excluir_id: al actualizar, no contar al propio servicio."""
        ...

    @abstractmethod
    def esta_en_uso(self, servicio_id: int) -> bool:
        """True si algun detalle de reserva usa este servicio."""
        ...

    @abstractmethod
    def guardar(self, servicio: ServicioExtra) -> ServicioExtra:
        """Crea el servicio si no tiene id, o lo actualiza si ya existe."""
        ...

    @abstractmethod
    def eliminar(self, servicio_id: int) -> bool:
        ...