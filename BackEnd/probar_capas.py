"""
Prueba rapida de las capas de huespedes y cabanas contra TU esquema de Oracle.
Se ejecuta desde BackEnd/ con el entorno activo:

    python manage.py shell -c "exec(open('probar_capas.py', encoding='utf-8').read())"

Crea registros de prueba (documento PRUEBA-1, codigo PRUEBA-CAB), comprueba los
casos de uso y los BORRA al final. No toca tus datos de ejemplo.
"""

from decimal import Decimal
from django.core.exceptions import FieldError
from reservas.application.exceptions import (
    DocumentoDuplicadoError, HuespedNoEncontradoError, CodigoCabanaDuplicadoError,
    CabanaInvalidaError,
)
from reservas.application.use_cases import (
    CrearHuespedUseCase, ActualizarHuespedUseCase, ObtenerHuespedUseCase, ListarHuespedesUseCase,
    EliminarHuespedUseCase, CrearCabanaUseCase, ActualizarCabanaUseCase, ListarCabanasUseCase,
    EliminarCabanaUseCase,
)
from reservas.infrastructure.di import get_huesped_repository, get_cabana_repository
from reservas.infrastructure.models import HuespedModel, CabanaModel


def debe_fallar(exc, fn, *args):
    try:
        fn(*args)
    except exc as e:
        return str(e)
    raise AssertionError(f"debia lanzar {exc.__name__}")


h, c = get_huesped_repository(), get_cabana_repository()
HuespedModel.objects.filter(documento="PRUEBA-1").delete()
CabanaModel.objects.filter(codigo="PRUEBA-CAB").delete()
try:
    print("Huespedes en tu esquema:", len(ListarHuespedesUseCase(h).ejecutar()))
    print("Cabanas en tu esquema  :", len(ListarCabanasUseCase(c).ejecutar()))

    hu = CrearHuespedUseCase(h).ejecutar({"documento": "PRUEBA-1", "nombre": "Huésped de prueba", "pais": "Chile"})
    print("Huesped creado, id =", hu.id)
    print("Duplicado           :", debe_fallar(DocumentoDuplicadoError, CrearHuespedUseCase(h).ejecutar,
                                            {"documento": "PRUEBA-1", "nombre": "x", "pais": "Chile"}))
    ActualizarHuespedUseCase(h).ejecutar(hu.id, {"nombre": "Huésped actualizado"})
    assert ObtenerHuespedUseCase(h).ejecutar(hu.id).nombre == "Huésped actualizado"
    print("No encontrado       :", debe_fallar(HuespedNoEncontradoError, ObtenerHuespedUseCase(h).ejecutar, 999999))

    ca = CrearCabanaUseCase(c).ejecutar({"codigo": "PRUEBA-CAB", "nombre": "Cabaña de prueba", "capacidad": 4, "valor_noche": 50000})
    print("Cabana creada, id   =", ca.id, "| admite 5 personas:", ca.admite(5), "| 3 noches:", ca.costo_estadia(3))
    print("Codigo duplicado    :", debe_fallar(CodigoCabanaDuplicadoError, CrearCabanaUseCase(c).ejecutar,
                                            {"codigo": "PRUEBA-CAB", "nombre": "x", "capacidad": 2, "valor_noche": 1}))
    print("Capacidad invalida  :", debe_fallar(CabanaInvalidaError, CrearCabanaUseCase(c).ejecutar,
                                            {"codigo": "OTRA", "nombre": "x", "capacidad": 0, "valor_noche": 1}))
    ActualizarCabanaUseCase(c).ejecutar(ca.id, {"valor_noche": 55000})

    try:
        EliminarHuespedUseCase(h).ejecutar(hu.id)
        EliminarCabanaUseCase(c).ejecutar(ca.id)
        print("Borrado con los casos de uso: OK")
    except FieldError:
        print("PENDIENTE: falta el ReservaModel de Brayan (relacion 'reservas'); "
              "el borrado protegido se prueba cuando lo suba.")
    print("\nOK: las capas de huespedes y cabanas funcionan.")
finally:
    HuespedModel.objects.filter(documento="PRUEBA-1").delete()
    CabanaModel.objects.filter(codigo="PRUEBA-CAB").delete()
