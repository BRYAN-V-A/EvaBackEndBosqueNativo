"""Casos de uso de Cabana."""

from decimal import Decimal
from typing import List
from reservas.domain.entities import Cabana
from reservas.domain.repositories import CabanaRepository
from reservas.application.exceptions import (
    CabanaNoEncontradaError, CodigoCabanaDuplicadoError, CabanaConReservasError,
    CabanaInvalidaError,
)


def _validar_datos(capacidad: int, valor_noche: Decimal) -> None:
    """Segundo nivel de validacion (el primero son los CHECK de Oracle):
    asi un dato invalido da un error de negocio claro y no un error 500."""
    if capacidad < 1:
        raise CabanaInvalidaError("La capacidad debe ser de al menos 1 persona")
    if valor_noche < 0:
        raise CabanaInvalidaError("El valor por noche no puede ser negativo")


class ListarCabanasUseCase:
    def __init__(self, repo: CabanaRepository):
        self.repo = repo

    def ejecutar(self) -> List[Cabana]:
        return self.repo.listar()


class ObtenerCabanaUseCase:
    def __init__(self, repo: CabanaRepository):
        self.repo = repo

    def ejecutar(self, cabana_id: int) -> Cabana:
        cabana = self.repo.obtener_por_id(cabana_id)
        if cabana is None:
            raise CabanaNoEncontradaError(f"No existe una cabaña con id {cabana_id}")
        return cabana


class CrearCabanaUseCase:
    def __init__(self, repo: CabanaRepository):
        self.repo = repo

    def ejecutar(self, datos: dict) -> Cabana:
        capacidad = int(datos["capacidad"])
        valor_noche = Decimal(str(datos["valor_noche"]))
        _validar_datos(capacidad, valor_noche)
        if self.repo.existe_codigo(datos["codigo"]):
            raise CodigoCabanaDuplicadoError(f"Ya existe una cabaña con el código {datos['codigo']}")

        cabana = Cabana(
            codigo=datos["codigo"], nombre=datos["nombre"], capacidad=capacidad,
            valor_noche=valor_noche, activa=datos.get("activa", True),
        )
        return self.repo.guardar(cabana)


class ActualizarCabanaUseCase:
    def __init__(self, repo: CabanaRepository):
        self.repo = repo

    def ejecutar(self, cabana_id: int, datos: dict) -> Cabana:
        cabana = ObtenerCabanaUseCase(self.repo).ejecutar(cabana_id)

        cabana.codigo = datos.get("codigo", cabana.codigo)
        cabana.nombre = datos.get("nombre", cabana.nombre)
        cabana.capacidad = int(datos.get("capacidad", cabana.capacidad))
        cabana.valor_noche = Decimal(str(datos.get("valor_noche", cabana.valor_noche)))
        cabana.activa = datos.get("activa", cabana.activa)

        _validar_datos(cabana.capacidad, cabana.valor_noche)
        if self.repo.existe_codigo(cabana.codigo, excluir_id=cabana_id):
            raise CodigoCabanaDuplicadoError(f"Ya existe una cabaña con el código {cabana.codigo}")
        return self.repo.guardar(cabana)


class EliminarCabanaUseCase:
    def __init__(self, repo: CabanaRepository):
        self.repo = repo

    def ejecutar(self, cabana_id: int) -> None:
        ObtenerCabanaUseCase(self.repo).ejecutar(cabana_id)
        if self.repo.tiene_reservas(cabana_id):
            raise CabanaConReservasError(
                "No se puede eliminar una cabaña que tiene reservas (desactívala con activa=false)"
            )
        self.repo.eliminar(cabana_id)
