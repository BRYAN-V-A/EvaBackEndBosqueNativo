"""Casos de uso de Huesped. Aca ni siquiera se conoce COMO se guardan los
datos, solo el contrato (HuespedRepository)."""

from typing import List
from reservas.domain.entities import Huesped
from reservas.domain.repositories import HuespedRepository
from reservas.application.exceptions import (
    DocumentoDuplicadoError, HuespedNoEncontradoError, HuespedConReservasError,
)


def _validar_unicos(repo: HuespedRepository, documento: str, excluir_id=None) -> None:
    """El rut o pasaporte no se puede repetir entre huespedes."""
    if repo.existe_documento(documento, excluir_id):
        raise DocumentoDuplicadoError(f"Ya existe un huésped con el documento {documento}")


class ListarHuespedesUseCase:
    def __init__(self, repo: HuespedRepository):
        self.repo = repo

    def ejecutar(self) -> List[Huesped]:
        return self.repo.listar()


class ObtenerHuespedUseCase:
    def __init__(self, repo: HuespedRepository):
        self.repo = repo

    def ejecutar(self, huesped_id: int) -> Huesped:
        huesped = self.repo.obtener_por_id(huesped_id)
        if huesped is None:
            raise HuespedNoEncontradoError(f"No existe un huésped con id {huesped_id}")
        return huesped


class CrearHuespedUseCase:
    def __init__(self, repo: HuespedRepository):
        self.repo = repo

    def ejecutar(self, datos: dict) -> Huesped:
        _validar_unicos(self.repo, datos["documento"])

        huesped = Huesped(
            documento=datos["documento"], nombre=datos["nombre"], pais=datos["pais"],
            email=datos.get("email"),
        )
        return self.repo.guardar(huesped)


class ActualizarHuespedUseCase:
    def __init__(self, repo: HuespedRepository):
        self.repo = repo

    def ejecutar(self, huesped_id: int, datos: dict) -> Huesped:
        huesped = ObtenerHuespedUseCase(self.repo).ejecutar(huesped_id)

        huesped.documento = datos.get("documento", huesped.documento)
        huesped.nombre = datos.get("nombre", huesped.nombre)
        huesped.pais = datos.get("pais", huesped.pais)
        huesped.email = datos.get("email", huesped.email)
        _validar_unicos(self.repo, huesped.documento, excluir_id=huesped_id)
        return self.repo.guardar(huesped)


class EliminarHuespedUseCase:
    def __init__(self, repo: HuespedRepository):
        self.repo = repo

    def ejecutar(self, huesped_id: int) -> None:
        ObtenerHuespedUseCase(self.repo).ejecutar(huesped_id)
        if self.repo.tiene_reservas(huesped_id):
            raise HuespedConReservasError("No se puede eliminar un huésped que tiene reservas")
        self.repo.eliminar(huesped_id)
