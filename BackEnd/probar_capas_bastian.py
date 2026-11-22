# Prueba rapida de las capas de servicios_extra contra Oracle (FreeSQL).
# Desde la carpeta BackEnd, con el entorno activado:
#   python manage.py shell -c "exec(open('probar_capas_bastian.py', encoding='utf-8').read())"
from decimal import Decimal
from reservas.infrastructure.di import get_servicio_extra_repository
from reservas.application.use_cases import *
from reservas.application.exceptions import *


def debe_fallar(exc, fn, *a):
    try:
        fn(*a)
    except exc as e:
        return str(e)
    raise AssertionError(f"debia lanzar {exc.__name__}")


repo = get_servicio_extra_repository()
creado = None
try:
    creado = CrearServicioUseCase(repo).ejecutar({"nombre": "PRUEBA-Tinaja", "precio": "35000.50"})
    assert creado.id and creado.precio == Decimal("35000.50")
    assert creado.subtotal(2) == Decimal("70001.00")
    print("Creado:", creado.id, creado.nombre)
    print("Duplicado :", debe_fallar(ServicioDuplicadoError, CrearServicioUseCase(repo).ejecutar, {"nombre": "PRUEBA-Tinaja", "precio": 1}))
    print("Precio <0 :", debe_fallar(ServicioInvalidoError, CrearServicioUseCase(repo).ejecutar, {"nombre": "PRUEBA-X", "precio": -1}))
    act = ActualizarServicioUseCase(repo).ejecutar(creado.id, {"precio": 40000})
    assert act.precio == Decimal("40000")
    print("No existe :", debe_fallar(ServicioNoEncontradoError, ObtenerServicioUseCase(repo).ejecutar, -1))
    assert any(s.id == creado.id for s in ListarServiciosUseCase(repo).ejecutar())
    print("TODO OK")
finally:
    if creado:
        repo.eliminar(creado.id)
