"""
Modelos de Django ORM: un archivo por tabla. OJO: esto NO es el
dominio, es el detalle de persistencia - la UNICA parte del proyecto
que sabe que existe Oracle. Solo se usan aca adentro (infrastructure/)
y en admin.py; el resto de la app solo conoce las entidades de
domain/entities/.

Todas las tablas YA EXISTEN en tu esquema de Oracle (las crea el
script sql/01_crear_tablas.sql, no Django): managed = False hace que
las migraciones no las creen, modifiquen ni borren. db_table dice el
nombre exacto de cada tabla.

Se importan todos aca para que Django los registre.
OJO (trabajo en equipo): cada integrante agrega SUS lineas de import.
"""

from .huesped import HuespedModel
from .cabana import CabanaModel
from .servicio_extra import ServicioExtraModel