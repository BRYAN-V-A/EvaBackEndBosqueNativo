from django.db import models


class CabanaModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_cabana")
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    valor_noche = models.DecimalField(max_digits=10, decimal_places=2)
    # En Oracle es NUMBER(1) con CHECK (0 o 1); Django lo maneja como booleano
    activa = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "cabanas"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
