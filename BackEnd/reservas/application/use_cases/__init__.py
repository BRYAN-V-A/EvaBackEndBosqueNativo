"""
APPLICATION RING (Casos de uso)
----------------------------------
Un archivo de casos de uso por tabla. Aca vive la LOGICA DE NEGOCIO:
que se hace con cada peticion, en que orden y que reglas se validan.
Cada caso de uso recibe el repositorio (el puerto, no una
implementacion concreta) por constructor -> inyeccion de dependencias.

OJO (trabajo en equipo): cada integrante agrega SUS lineas de import.
"""

from .huesped_use_cases import (
    ListarHuespedesUseCase, ObtenerHuespedUseCase, CrearHuespedUseCase,
    ActualizarHuespedUseCase, EliminarHuespedUseCase,
)
from .cabana_use_cases import (
    ListarCabanasUseCase, ObtenerCabanaUseCase, CrearCabanaUseCase,
    ActualizarCabanaUseCase, EliminarCabanaUseCase,
)
