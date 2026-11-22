from django.db import models
from .huesped import HuespedModel
from .cabana import CabanaModel


class ReservaModel(models.Model):
    ESTADOS = [("pendiente", "Pendiente"), ("confirmada", "Confirmada"),
               ("finalizada", "Finalizada"), ("cancelada", "Cancelada")]

    id = models.AutoField(primary_key=True, db_column="id_reserva")
    huesped = models.ForeignKey(
        HuespedModel, on_delete=models.PROTECT, db_column="id_huesped", related_name="reservas",
    )
    cabana = models.ForeignKey(
        CabanaModel, on_delete=models.PROTECT, db_column="id_cabana", related_name="reservas",
    )
    fecha_llegada = models.DateField()
    fecha_salida = models.DateField()
    n_personas = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="pendiente")

    class Meta:
        managed = False
        db_table = "reservas"

    def __str__(self):
        return f"Reserva {self.id} - {self.estado}"
