"""Puerto de salida para Cabana."""

from abc import ABC, abstractmethod
from typing import List, Optional
from reservas.domain.entities import Cabana


class CabanaRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Cabana]:
        ...

    @abstractmethod
    def obtener_por_id(self, cabana_id: int) -> Optional[Cabana]:
        ...

    @abstractmethod
    def existe_codigo(self, codigo: str, excluir_id: Optional[int] = None) -> bool:
        """excluir_id: al actualizar, no contar a la propia cabana."""
        ...

    @abstractmethod
    def tiene_reservas(self, cabana_id: int) -> bool:
        ...

    @abstractmethod
    def guardar(self, cabana: Cabana) -> Cabana:
        """Crea la cabana si no tiene id, o la actualiza si ya existe."""
        ...

    @abstractmethod
    def eliminar(self, cabana_id: int) -> bool:
        ...
