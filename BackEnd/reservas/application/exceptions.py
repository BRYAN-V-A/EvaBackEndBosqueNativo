"""Excepciones propias del dominio/aplicacion, sin depender de
Django ni de DRF. La capa adaptadores/ las traduce a codigos
HTTP (400, 404, 409), pero aca no se sabe que existe HTTP.

Tres grupos base. En la semana 5 cada grupo se traduce a un codigo HTTP:
NoEncontradoError -> 404, DuplicadoError -> 409, ReglaNegocioError -> 409.

ARCHIVO COMPARTIDO: lo sube Bastian primero; los demas lo importan.
"""


class NoEncontradoError(Exception):
    """El registro pedido no existe -> 404"""


class DuplicadoError(Exception):
    """Un dato que debe ser unico ya esta usado -> 409"""


class ReglaNegocioError(Exception):
    """La operacion no esta permitida por una regla de negocio -> 409"""


# --- Huespedes
class HuespedNoEncontradoError(NoEncontradoError):
    pass


class DocumentoDuplicadoError(DuplicadoError):
    pass


class HuespedConReservasError(ReglaNegocioError):
    pass


# --- Cabanas
class CabanaNoEncontradaError(NoEncontradoError):
    pass


class CodigoCabanaDuplicadoError(DuplicadoError):
    pass


class CabanaConReservasError(ReglaNegocioError):
    pass


class CabanaInvalidaError(ReglaNegocioError):
    """Capacidad menor a 1 o valor por noche negativo."""


# --- Servicios extra
class ServicioNoEncontradoError(NoEncontradoError):
    pass


class ServicioDuplicadoError(DuplicadoError):
    pass


class ServicioEnUsoError(ReglaNegocioError):
    pass


# --- Reservas
class ReservaNoEncontradaError(NoEncontradoError):
    pass


class FechasCruzadasError(ReglaNegocioError):
    """R1: la cabana ya tiene una reserva no cancelada en esas fechas."""


class CapacidadExcedidaError(ReglaNegocioError):
    """R2: mas personas que la capacidad de la cabana."""


class EstadiaMinimaError(ReglaNegocioError):
    """R3: la reserva es de menos de 2 noches."""


class ReservaInvalidaError(ReglaNegocioError):
    """Cabana inactiva, servicio repetido, fechas incoherentes..."""


class CambioEstadoInvalidoError(ReglaNegocioError):
    pass
