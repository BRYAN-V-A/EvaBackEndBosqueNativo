"""Casos de uso de Reserva.
Aca viven las reglas que NECESITAN datos de otras tablas:
  R1  sin cruce de fechas      -> reserva_repo.hay_cruce()
  R2  capacidad de la cabana   -> Cabana.admite()
  R3  total y minimo 2 noches  -> Reserva.cumple_estadia_minima() / calcular_total()
El caso de uso solo conoce los PUERTOS."""

from datetime import date
from typing import List
from reservas.domain.entities import Reserva, DetalleServicio, ESTADOS_RESERVA
from reservas.domain.repositories import (
    ReservaRepository, HuespedRepository, CabanaRepository, ServicioExtraRepository,
)
from reservas.application.exceptions import (
    HuespedNoEncontradoError, CabanaNoEncontradaError, ServicioNoEncontradoError,
    ReservaNoEncontradaError, FechasCruzadasError, CapacidadExcedidaError,
    EstadiaMinimaError, ReservaInvalidaError, CambioEstadoInvalidoError,
)


def _a_fecha(valor, campo: str) -> date:
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        raise ReservaInvalidaError(f"{campo} no es una fecha valida (use AAAA-MM-DD)")


class ListarReservasUseCase:
    def __init__(self, repo: ReservaRepository):
        self.repo = repo

    def ejecutar(self) -> List[Reserva]:
        return self.repo.listar()


class ObtenerReservaUseCase:
    def __init__(self, repo: ReservaRepository):
        self.repo = repo

    def ejecutar(self, reserva_id: int) -> Reserva:
        reserva = self.repo.obtener_por_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(f"No existe una reserva con id {reserva_id}")
        return reserva


class CrearReservaUseCase:

    def __init__(self, reserva_repo: ReservaRepository, huesped_repo: HuespedRepository,
                 cabana_repo: CabanaRepository, servicio_repo: ServicioExtraRepository):
        self.reserva_repo = reserva_repo
        self.huesped_repo = huesped_repo
        self.cabana_repo = cabana_repo
        self.servicio_repo = servicio_repo

    def ejecutar(self, datos: dict) -> Reserva:
        llegada = _a_fecha(datos["fecha_llegada"], "fecha_llegada")
        salida = _a_fecha(datos["fecha_salida"], "fecha_salida")
        n_personas = int(datos["n_personas"])

        if salida <= llegada:
            raise ReservaInvalidaError("La fecha de salida debe ser posterior a la de llegada")

        if self.huesped_repo.obtener_por_id(datos["huesped_id"]) is None:
            raise HuespedNoEncontradoError(f"No existe un huesped con id {datos['huesped_id']}")
        cabana = self.cabana_repo.obtener_por_id(datos["cabana_id"])
        if cabana is None:
            raise CabanaNoEncontradaError(f"No existe una cabaña con id {datos['cabana_id']}")
        if not cabana.activa:
            raise ReservaInvalidaError("La cabaña está inactiva y no se puede reservar")

        detalles, vistos = [], set()
        for item in datos.get("servicios", []):
            servicio_id, cantidad = item["servicio_id"], int(item["cantidad"])
            if cantidad < 1:
                raise ReservaInvalidaError("La cantidad de un servicio debe ser al menos 1")
            if servicio_id in vistos:
                raise ReservaInvalidaError(f"El servicio {servicio_id} está repetido en la reserva")
            vistos.add(servicio_id)
            servicio = self.servicio_repo.obtener_por_id(servicio_id)
            if servicio is None:
                raise ServicioNoEncontradoError(f"No existe un servicio con id {servicio_id}")
            detalles.append(DetalleServicio(
                servicio_id=servicio_id, cantidad=cantidad, precio_unitario=servicio.precio,
            ))

        reserva = Reserva(
            huesped_id=datos["huesped_id"], cabana_id=cabana.id,
            fecha_llegada=llegada, fecha_salida=salida,
            n_personas=n_personas, detalles=detalles,
        )

        if not reserva.cumple_estadia_minima():
            raise EstadiaMinimaError(
                f"La estadía mínima es de 2 noches (se pidieron {reserva.noches()})"
            )
        
        if not cabana.admite(n_personas):
            raise CapacidadExcedidaError(
                f"La cabaña {cabana.codigo} admite hasta {cabana.capacidad} personas "
                f"(se pidieron {n_personas})"
            )
        
        if self.reserva_repo.hay_cruce(cabana.id, llegada, salida):
            raise FechasCruzadasError(
                f"La cabaña {cabana.codigo} ya está reservada entre {llegada} y {salida}"
            )

        reserva.total = reserva.calcular_total(cabana.valor_noche)
        return self.reserva_repo.registrar(reserva)


class CambiarEstadoReservaUseCase:

    def __init__(self, repo: ReservaRepository):
        self.repo = repo

    def ejecutar(self, reserva_id: int, nuevo_estado: str) -> Reserva:
        if nuevo_estado not in ESTADOS_RESERVA:
            raise CambioEstadoInvalidoError(f"Estado desconocido: {nuevo_estado}")
        reserva = ObtenerReservaUseCase(self.repo).ejecutar(reserva_id)
        if not reserva.puede_pasar_a(nuevo_estado):
            raise CambioEstadoInvalidoError(
                f"No se puede pasar de {reserva.estado} a {nuevo_estado}"
            )
        return self.repo.cambiar_estado(reserva, nuevo_estado)


class EliminarReservaUseCase:

    def __init__(self, repo: ReservaRepository):
        self.repo = repo

    def ejecutar(self, reserva_id: int) -> None:
        reserva = ObtenerReservaUseCase(self.repo).ejecutar(reserva_id)
        if reserva.estado != "pendiente":
            raise CambioEstadoInvalidoError(
                f"Solo se puede eliminar una reserva pendiente (esta está {reserva.estado})"
            )
        self.repo.eliminar(reserva_id)
