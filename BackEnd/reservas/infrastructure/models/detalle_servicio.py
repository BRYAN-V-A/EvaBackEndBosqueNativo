from django.db import models
from .reserva import ReservaModel
from .servicio_extra import ServicioExtraModel


class DetalleServicioModel(models.Model):
    pk = models.CompositePrimaryKey("reserva", "servicio")
    reserva = models.ForeignKey(
        ReservaModel, on_delete=models.CASCADE, db_column="id_reserva", related_name="detalles",
    )
    servicio = models.ForeignKey(
        ServicioExtraModel, on_delete=models.PROTECT, db_column="id_servicio", related_name="detalles",
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.GeneratedField(
        expression=models.F("cantidad") * models.F("precio_unitario"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=False,
    )

    class Meta:
        managed = False
        db_table = "detalle_servicio"

    def __str__(self):
        return f"Reserva {self.reserva_id} - servicio {self.servicio_id} x {self.cantidad}"
