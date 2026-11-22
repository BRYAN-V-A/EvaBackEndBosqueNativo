"""Puerto de salida para Huesped. Hoy lo implementa Django ORM + Oracle;
manana podria ser otra base, sin que la logica de negocio se entere."""

from abc import ABC, abstractmethod
from typing import List, Optional
from reservas.domain.entities import Huesped


class HuespedRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Huesped]:
        ...

    @abstractmethod
    def obtener_por_id(self, huesped_id: int) -> Optional[Huesped]:
        ...

    @abstractmethod
    def existe_documento(self, documento: str, excluir_id: Optional[int] = None) -> bool:
        """excluir_id: al actualizar, no contar al propio huesped."""
        ...

    @abstractmethod
    def tiene_reservas(self, huesped_id: int) -> bool:
        ...

    @abstractmethod
    def guardar(self, huesped: Huesped) -> Huesped:
        """Crea el huesped si no tiene id, o lo actualiza si ya existe."""
        ...

    @abstractmethod
    def eliminar(self, huesped_id: int) -> bool:
        ...
