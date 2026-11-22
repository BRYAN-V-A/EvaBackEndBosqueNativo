from typing import List, Optional
from reservas.domain.entities import Huesped
from reservas.domain.repositories import HuespedRepository
from reservas.infrastructure.models import HuespedModel


def _to_entity(m: HuespedModel) -> Huesped:
    return Huesped(id=m.id, documento=m.documento, nombre=m.nombre, pais=m.pais, email=m.email)


class DjangoHuespedRepository(HuespedRepository):

    def listar(self) -> List[Huesped]:
        return [_to_entity(m) for m in HuespedModel.objects.order_by("nombre")]

    def obtener_por_id(self, huesped_id: int) -> Optional[Huesped]:
        m = HuespedModel.objects.filter(id=huesped_id).first()
        return _to_entity(m) if m else None

    def existe_documento(self, documento: str, excluir_id: Optional[int] = None) -> bool:
        return HuespedModel.objects.filter(documento=documento).exclude(id=excluir_id).exists()

    def tiene_reservas(self, huesped_id: int) -> bool:
        # Usa la relacion inversa "reservas" que declara ReservaModel (Brayan):
        # ReservaModel.huesped = ForeignKey(HuespedModel, related_name="reservas", ...)
        return HuespedModel.objects.filter(id=huesped_id, reservas__isnull=False).exists()

    def guardar(self, huesped: Huesped) -> Huesped:
        if huesped.id is None:
            m = HuespedModel.objects.create(
                documento=huesped.documento, nombre=huesped.nombre,
                email=huesped.email, pais=huesped.pais,
            )
        else:
            m = HuespedModel.objects.get(id=huesped.id)
            m.documento, m.nombre = huesped.documento, huesped.nombre
            m.email, m.pais = huesped.email, huesped.pais
            m.save(update_fields=["documento", "nombre", "email", "pais"])
        return _to_entity(m)

    def eliminar(self, huesped_id: int) -> bool:
        borrados, _ = HuespedModel.objects.filter(id=huesped_id).delete()
        return borrados > 0
