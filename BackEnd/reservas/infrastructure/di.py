"""
Contenedor de inyeccion de dependencias, MUY simple. Es el unico
lugar de todo el proyecto que "decide" que implementacion concreta
de cada repositorio se usa. Los casos de uso y los adaptadores de
entrada nunca instancian un DjangoXxxRepository directamente - piden
el repositorio a estas funciones.

OJO (trabajo en equipo): este archivo lo completa Bastian al final; aca
van solo las funciones de huespedes y cabanas.
"""

from .repositories import DjangoHuespedRepository, DjangoCabanaRepository, DjangoServicioExtraRepository
from .repositories import DjangoReservaRepository


def get_huesped_repository():
    return DjangoHuespedRepository()

def get_cabana_repository():
    return DjangoCabanaRepository()

def get_servicio_extra_repository():
    return DjangoServicioExtraRepository()

def get_reserva_repository():
    return DjangoReservaRepository()