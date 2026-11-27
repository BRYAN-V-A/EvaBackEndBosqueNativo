# Prueba de los casos de uso de reservas (R1, R2, R3, estados) contra Oracle.
# Desde la carpeta BackEnd, con el entorno activado:
#   python manage.py shell -c "exec(open('probar_casos_uso_bryan.py', encoding='utf-8').read())"
# Crea datos PRUEBA-*, los usa y los borra al final.
from decimal import Decimal
from reservas.infrastructure.di import (
    get_huesped_repository, get_cabana_repository,
    get_servicio_extra_repository, get_reserva_repository,
)
from reservas.application.use_cases import (
    CrearHuespedUseCase, CrearCabanaUseCase, CrearServicioUseCase,
    CrearReservaUseCase, CambiarEstadoReservaUseCase, EliminarReservaUseCase,
)
from reservas.application.exceptions import (
    EstadiaMinimaError, CapacidadExcedidaError, FechasCruzadasError,
    ReservaInvalidaError, CambioEstadoInvalidoError,
)


def debe_fallar(exc, fn, *a):
    try:
        fn(*a)
    except exc as e:
        return str(e)
    raise AssertionError(f"debia lanzar {exc.__name__}")


h, c, s, r = (get_huesped_repository(), get_cabana_repository(),
              get_servicio_extra_repository(), get_reserva_repository())
huesped = cabana = servicio = None
reservas = []
try:
    huesped = CrearHuespedUseCase(h).ejecutar({"documento": "PRUEBA-R1", "nombre": "Prueba Reservas", "pais": "Chile"})
    cabana = CrearCabanaUseCase(c).ejecutar({"codigo": "PRUEBA-CABR", "nombre": "Cabana prueba", "capacidad": 4, "valor_noche": 50000})
    servicio = CrearServicioUseCase(s).ejecutar({"nombre": "PRUEBA-Tinaja", "precio": 20000})
    crear = CrearReservaUseCase(r, h, c, s)
    base = {"huesped_id": huesped.id, "cabana_id": cabana.id, "n_personas": 2,
            "fecha_llegada": "2030-03-10", "fecha_salida": "2030-03-13"}

    g = crear.ejecutar({**base, "servicios": [{"servicio_id": servicio.id, "cantidad": 2}]})
    reservas.append(g.id)
    assert g.total == Decimal("190000"), g.total          # 3 x 50000 + 2 x 20000
    print("R3 total (3 noches + 2 servicios):", g.total, "OK")
    print("R3 minimo de noches:", debe_fallar(EstadiaMinimaError, crear.ejecutar, {**base, "fecha_llegada": "2030-04-01", "fecha_salida": "2030-04-02"}))
    print("R2 capacidad       :", debe_fallar(CapacidadExcedidaError, crear.ejecutar, {**base, "n_personas": 9, "fecha_llegada": "2030-04-01", "fecha_salida": "2030-04-04"}))
    print("R1 cruce de fechas :", debe_fallar(FechasCruzadasError, crear.ejecutar, {**base, "fecha_llegada": "2030-03-12", "fecha_salida": "2030-03-15"}))
    print("Servicio repetido  :", debe_fallar(ReservaInvalidaError, crear.ejecutar, {**base, "fecha_llegada": "2030-05-01", "fecha_salida": "2030-05-04", "servicios": [{"servicio_id": servicio.id, "cantidad": 1}, {"servicio_id": servicio.id, "cantidad": 1}]}))
    cambiar = CambiarEstadoReservaUseCase(r)
    print("Pendiente -> finalizada:", debe_fallar(CambioEstadoInvalidoError, cambiar.ejecutar, g.id, "finalizada"))
    assert cambiar.ejecutar(g.id, "confirmada").estado == "confirmada"
    print("Confirmada no se elimina:", debe_fallar(CambioEstadoInvalidoError, EliminarReservaUseCase(r).ejecutar, g.id))
    assert cambiar.ejecutar(g.id, "cancelada").estado == "cancelada"
    otra = crear.ejecutar(base)                           # la cancelada liberó la cabaña
    reservas.append(otra.id)
    print("Cancelada libera la cabana: OK")
    print("TODO OK")
finally:
    for rid in reservas:
        r.eliminar(rid)
    if cabana: c.eliminar(cabana.id)
    if huesped: h.eliminar(huesped.id)
    if servicio: s.eliminar(servicio.id)
