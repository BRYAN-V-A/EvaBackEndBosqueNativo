from datetime import date
from typing import List, Optional
from django.db import router, transaction
from reservas.domain.entities import Reserva, DetalleServicio
from reservas.domain.repositories import ReservaRepository
from reservas.infrastructure.models import ReservaModel, DetalleServicioModel


def _to_entity(m: ReservaModel) -> Reserva:
    detalles = [
        DetalleServicio(
            reserva_id=d.reserva_id, servicio_id=d.servicio_id,
            cantidad=d.cantidad, precio_unitario=d.precio_unitario,
        )
        for d in m.detalles.all()
    ]
    return Reserva(
        id=m.id, huesped_id=m.huesped_id, cabana_id=m.cabana_id,
        fecha_llegada=m.fecha_llegada, fecha_salida=m.fecha_salida,
        n_personas=m.n_personas, total=m.total, estado=m.estado, detalles=detalles,
    )


def _atomic():
    return transaction.atomic(using=router.db_for_write(ReservaModel))


class DjangoReservaRepository(ReservaRepository):

    def listar(self) -> List[Reserva]:
        reservas = ReservaModel.objects.prefetch_related("detalles").order_by("-id")
        return [_to_entity(m) for m in reservas]

    def obtener_por_id(self, reserva_id: int) -> Optional[Reserva]:
        m = ReservaModel.objects.prefetch_related("detalles").filter(id=reserva_id).first()
        return _to_entity(m) if m else None

    def hay_cruce(self, cabana_id: int, llegada: date, salida: date,
                  excluir_id: Optional[int] = None) -> bool:

        return (
            ReservaModel.objects
            .filter(cabana_id=cabana_id, fecha_llegada__lt=salida, fecha_salida__gt=llegada)
            .exclude(estado="cancelada")
            .exclude(id=excluir_id)
            .exists()
        )

    def registrar(self, reserva: Reserva) -> Reserva:
        with _atomic():
            m = ReservaModel.objects.create(
                huesped_id=reserva.huesped_id, cabana_id=reserva.cabana_id,
                fecha_llegada=reserva.fecha_llegada, fecha_salida=reserva.fecha_salida,
                n_personas=reserva.n_personas, total=reserva.total, estado=reserva.estado,
            )
            for d in reserva.detalles:
                DetalleServicioModel.objects.create(
                    reserva=m, servicio_id=d.servicio_id,
                    cantidad=d.cantidad, precio_unitario=d.precio_unitario,
                )
        return self.obtener_por_id(m.id)

    def cambiar_estado(self, reserva: Reserva, nuevo_estado: str) -> Reserva:
        ReservaModel.objects.filter(id=reserva.id).update(estado=nuevo_estado)
        return self.obtener_por_id(reserva.id)

    def eliminar(self, reserva_id: int) -> bool:
        borrados, _ = ReservaModel.objects.filter(id=reserva_id).delete()
        return borrados > 0
