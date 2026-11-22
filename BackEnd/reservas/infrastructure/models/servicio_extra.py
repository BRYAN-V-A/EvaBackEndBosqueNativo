from django.db import models


class ServicioExtraModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_servicio")
    nombre = models.CharField(max_length=60, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False            # la tabla ya la creo el script SQL
        db_table = "servicios_extra"

    def __str__(self):
        return self.nombre
