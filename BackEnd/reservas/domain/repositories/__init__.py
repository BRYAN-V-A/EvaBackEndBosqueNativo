"""
PUERTOS (Ports) de salida
---------------------------
Un contrato (interfaz abstracta) por tabla. El dominio y los casos de
uso dependen de ESTAS interfaces, nunca de Django ORM directamente
(principio de inversion de dependencias). Las implementaciones viven
en infrastructure/repositories/ (adaptadores secundarios).

OJO (trabajo en equipo): cada integrante agrega SUS lineas de import.
"""

from .huesped_repository import HuespedRepository
from .cabana_repository import CabanaRepository
from .servicio_extra_repository import ServicioExtraRepository
from .reserva_repository import ReservaRepository