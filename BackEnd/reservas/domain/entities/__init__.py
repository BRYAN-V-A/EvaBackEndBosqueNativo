"""
DOMINIO (Core Domain) - Entidades
-----------------------------------
Una entidad por archivo, una por cada tabla de la base. Son dataclasses
PUROS: no heredan de models.Model, no importan nada de Django y no saben
que existe Oracle ni HTTP. Quien habla con la base es infrastructure/.

Se re-exportan aca para poder escribir:
    from reservas.domain.entities import Huesped, Cabana

OJO (trabajo en equipo): este archivo lo editan los tres. Cada uno agrega SUS
lineas de import; si ya hay lineas de otro integrante, no las borres.
"""

from .huesped import Huesped
from .cabana import Cabana
from .servicio_extra import ServicioExtra