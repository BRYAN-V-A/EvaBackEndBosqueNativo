from typing import List, Optional
from reservas.domain.entities import Cabana
from reservas.domain.repositories import CabanaRepository
from reservas.infrastructure.models import CabanaModel

CAMPOS = ["codigo", "nombre", "capacidad", "valor_noche", "activa"]


def _to_entity(m: CabanaModel) -> Cabana:
    return Cabana(
        id=m.id, codigo=m.codigo, nombre=m.nombre, capacidad=m.capacidad,
        valor_noche=m.valor_noche, activa=m.activa,
    )


class DjangoCabanaRepository(CabanaRepository):

    def listar(self) -> List[Cabana]:
        return [_to_entity(m) for m in CabanaModel.objects.order_by("codigo")]

    def obtener_por_id(self, cabana_id: int) -> Optional[Cabana]:
        m = CabanaModel.objects.filter(id=cabana_id).first()
        return _to_entity(m) if m else None

    def existe_codigo(self, codigo: str, excluir_id: Optional[int] = None) -> bool:
        return CabanaModel.objects.filter(codigo=codigo).exclude(id=excluir_id).exists()

    def tiene_reservas(self, cabana_id: int) -> bool:
        # Usa la relacion inversa "reservas" que declara ReservaModel (Brayan):
        # ReservaModel.cabana = ForeignKey(CabanaModel, related_name="reservas", ...)
        return CabanaModel.objects.filter(id=cabana_id, reservas__isnull=False).exists()

    def guardar(self, cabana: Cabana) -> Cabana:
        valores = {campo: getattr(cabana, campo) for campo in CAMPOS}
        if cabana.id is None:
            m = CabanaModel.objects.create(**valores)
        else:
            m = CabanaModel.objects.get(id=cabana.id)
            for campo, valor in valores.items():
                setattr(m, campo, valor)
            m.save(update_fields=CAMPOS)
        return _to_entity(m)

    def eliminar(self, cabana_id: int) -> bool:
        borrados, _ = CabanaModel.objects.filter(id=cabana_id).delete()
        return borrados > 0
