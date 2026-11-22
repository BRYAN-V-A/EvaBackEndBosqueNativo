from django.db import models


class HuespedModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_huesped")
    documento = models.CharField(max_length=20, unique=True)   # rut o pasaporte
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pais = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = "huespedes"

    def __str__(self):
        return f"{self.nombre} ({self.documento})"
