"""Casos de uso de ServicioExtra."""

from decimal import Decimal
from typing import List
from reservas.domain.entities import ServicioExtra
from reservas.domain.repositories import ServicioExtraRepository
from reservas.application.exceptions import (
    ServicioNoEncontradoError, ServicioDuplicadoError, ServicioEnUsoError,
    ServicioInvalidoError,
)


def _validar(nombre: str, precio: Decimal) -> None:
    if not nombre or not nombre.strip():
        raise ServicioInvalidoError("El nombre es obligatorio")
    if len(nombre) > 60:
        raise ServicioInvalidoError("El nombre no puede superar los 60 caracteres")
    if precio < 0:
        raise ServicioInvalidoError("El precio no puede ser negativo")
    if precio > Decimal("99999999.99"):
        raise ServicioInvalidoError("El precio es demasiado alto")

class ListarServiciosUseCase:
    def __init__(self, repo: ServicioExtraRepository):
        self.repo = repo

    def ejecutar(self) -> List[ServicioExtra]:
        return self.repo.listar()


class ObtenerServicioUseCase:
    def __init__(self, repo: ServicioExtraRepository):
        self.repo = repo

    def ejecutar(self, servicio_id: int) -> ServicioExtra:
        servicio = self.repo.obtener_por_id(servicio_id)
        if servicio is None:
            raise ServicioNoEncontradoError(f"No existe un servicio con id {servicio_id}")
        return servicio


class CrearServicioUseCase:
    def __init__(self, repo: ServicioExtraRepository):
        self.repo = repo

    def ejecutar(self, datos: dict) -> ServicioExtra:
        precio = Decimal(str(datos["precio"]))
        _validar(datos["nombre"], precio)
        if self.repo.existe_nombre(datos["nombre"]):
            raise ServicioDuplicadoError(f"Ya existe un servicio llamado {datos['nombre']}")
        return self.repo.guardar(ServicioExtra(nombre=datos["nombre"], precio=precio))


class ActualizarServicioUseCase:
    def __init__(self, repo: ServicioExtraRepository):
        self.repo = repo

    def ejecutar(self, servicio_id: int, datos: dict) -> ServicioExtra:
        servicio = ObtenerServicioUseCase(self.repo).ejecutar(servicio_id)
        servicio.nombre = datos.get("nombre", servicio.nombre)
        servicio.precio = Decimal(str(datos.get("precio", servicio.precio)))

        _validar(servicio.nombre, servicio.precio)
        if self.repo.existe_nombre(servicio.nombre, excluir_id=servicio_id):
            raise ServicioDuplicadoError(f"Ya existe un servicio llamado {servicio.nombre}")
        return self.repo.guardar(servicio)


class EliminarServicioUseCase:
    def __init__(self, repo: ServicioExtraRepository):
        self.repo = repo

    def ejecutar(self, servicio_id: int) -> None:
        ObtenerServicioUseCase(self.repo).ejecutar(servicio_id)
        if self.repo.esta_en_uso(servicio_id):
            raise ServicioEnUsoError(
                "No se puede eliminar un servicio que ya fue contratado en una reserva"
            )
        self.repo.eliminar(servicio_id)