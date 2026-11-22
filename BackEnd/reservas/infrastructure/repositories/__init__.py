"""
ADAPTADORES SECUNDARIOS (Driven Adapters)
-------------------------------------------
Implementaciones CONCRETAS de los puertos de domain/repositories/
usando Django ORM + Oracle, una por tabla. Traducen entre la entidad
de dominio (dataclass puro) y el modelo de persistencia (models.Model).
Si manana cambias de motor de base de datos, o de ORM, SOLO se
reescriben estos archivos - los casos de uso y el dominio quedan intactos.

OJO (trabajo en equipo): cada integrante agrega SUS lineas de import.
"""

from .huesped_repository import DjangoHuespedRepository
from .cabana_repository import DjangoCabanaRepository
