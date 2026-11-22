from typing import List, Optional
from reservas.domain.entities import ServicioExtra
from reservas.domain.repositories import ServicioExtraRepository
from reservas.infrastructure.models import ServicioExtraModel

CAMPOS = ["nombre", "precio"]


def _to_entity(m: ServicioExtraModel) -> ServicioExtra:
    return ServicioExtra(id=m.id, nombre=m.nombre, precio=m.precio)


class DjangoServicioExtraRepository(ServicioExtraRepository):

    def listar(self) -> List[ServicioExtra]:
        return [_to_entity(m) for m in ServicioExtraModel.objects.order_by("nombre")]

    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioExtra]:
        m = ServicioExtraModel.objects.filter(id=servicio_id).first()
        return _to_entity(m) if m else None

    def existe_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        return ServicioExtraModel.objects.filter(nombre=nombre).exclude(id=excluir_id).exists()

    def esta_en_uso(self, servicio_id: int) -> bool:
        # Usa la relacion inversa "detalles" que declara DetalleServicioModel (Brayan):
        # DetalleServicioModel.servicio = ForeignKey(ServicioExtraModel, related_name="detalles", ...)
        return ServicioExtraModel.objects.filter(id=servicio_id, detalles__isnull=False).exists()

    def guardar(self, servicio: ServicioExtra) -> ServicioExtra:
        valores = {campo: getattr(servicio, campo) for campo in CAMPOS}
        if servicio.id is None:
            m = ServicioExtraModel.objects.create(**valores)
        else:
            m = ServicioExtraModel.objects.get(id=servicio.id)
            for campo, valor in valores.items():
                setattr(m, campo, valor)
            m.save(update_fields=CAMPOS)
        return _to_entity(m)

    def eliminar(self, servicio_id: int) -> bool:
        borrados, _ = ServicioExtraModel.objects.filter(id=servicio_id).delete()
        return borrados > 0
