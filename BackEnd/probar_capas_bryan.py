# Prueba rapida de las capas de reservas contra Oracle (FreeSQL).
# Ejecutar desde la carpeta BackEnd, con el entorno activado:
#   python manage.py shell -c "exec(open('probar_capas_bryan.py', encoding='utf-8').read())"
from datetime import date
from decimal import Decimal
from reservas.infrastructure.models import HuespedModel, CabanaModel, ReservaModel
from reservas.infrastructure.di import get_reserva_repository
from reservas.domain.entities import Reserva, DetalleServicio

try:
    from reservas.infrastructure.models import ServicioExtraModel
except ImportError:
    ServicioExtraModel = None
    print("PENDIENTE: falta el modelo ServicioExtraModel de Bastian; no se puede probar aun.")

if ServicioExtraModel:
    repo = get_reserva_repository()
    h = c = rid = None
    try:
        h = HuespedModel.objects.create(documento="PRUEBA-B1", nombre="Prueba Bryan", pais="Chile")
        c = CabanaModel.objects.create(codigo="PRUEBA-CABB", nombre="Cabana de prueba", capacidad=4, valor_noche=50000, activa=True)
        s = ServicioExtraModel.objects.first()
        assert s, "No hay servicios_extra en la base (carga sql/02_datos_ejemplo.sql)"
        llegada, salida = date(2030, 1, 10), date(2030, 1, 13)
        res = Reserva(h.id, c.id, llegada, salida, 2, [DetalleServicio(s.id, 2, s.precio)])
        res.total = res.calcular_total(c.valor_noche)
        g = repo.registrar(res); rid = g.id
        print("Reserva creada:", g.id, "total", g.total, "detalles", len(g.detalles))
        assert g.total == 3 * Decimal(c.valor_noche) + 2 * s.precio
        assert repo.hay_cruce(c.id, date(2030, 1, 12), date(2030, 1, 15))
        assert not repo.hay_cruce(c.id, salida, date(2030, 1, 15))
        print("Cruce de fechas (R1): OK")
        assert repo.cambiar_estado(g, "cancelada").estado == "cancelada"
        assert not repo.hay_cruce(c.id, llegada, salida)
        print("Cancelada libera la cabana: OK")
        print("TODO OK")
    finally:
        if rid: repo.eliminar(rid)
        if c: c.delete()
        if h: h.delete()
