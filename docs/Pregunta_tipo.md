# Preguntas tipo de la semana

## Semana 1 · Diseño, base de datos y conexión

### Carla Caro (huespedes, cabanas)
**Pregunta:** ¿Por qué `documento` en huespedes y `codigo` en cabanas tienen una restricción UNIQUE, y dónde se controla?

**Respuesta:** Porque no puede haber dos huéspedes con el mismo documento ni dos cabañas con el mismo código. En Oracle lo asegura la restricción UNIQUE de la tabla (`sql/01_crear_tablas.sql`). En la semana 2 los casos de uso lo revisan antes de guardar para devolver un error de negocio claro y no un error de la base.

### Bryan Vallejos (reservas, detalle_servicio)
**Pregunta:** ¿Por qué `detalle_servicio` no tiene un id propio y qué es la columna `subtotal`?

**Respuesta:** Su clave primaria es la pareja (id_reserva, id_servicio): un servicio aparece una sola vez por reserva, así que no hace falta otro id. Resuelve la relación muchos a muchos entre reservas y servicios_extra. `subtotal` es una columna virtual: Oracle la calcula como cantidad × precio_unitario y no se guarda ni se escribe desde Django.

### Bastián Saez (servicios_extra)
**Pregunta:** ¿Por qué el precio se guarda como NUMBER(10,2) y no como un número decimal común?

**Respuesta:** Porque es dinero y los decimales comunes (float) pueden dar errores de redondeo. NUMBER(10,2) guarda el valor exacto con dos decimales. En Python se usa `Decimal` por la misma razón. Además, un CHECK asegura que el precio no sea negativo.

## Semana 2 · Capas hexagonales de las entidades maestras

### Carla Caro (huespedes, cabanas)
**Pregunta:** ¿Qué pasa si intento borrar un huésped que tiene reservas?

**Respuesta:** El caso de uso le pregunta al repositorio si el huésped tiene reservas. Si las tiene, lanza `HuespedConReservasError` y no borra nada. El repositorio lo sabe usando la relación inversa `reservas` del modelo de reservas. Además, Oracle también lo impide con la clave foránea (PROTECT en el modelo).

### Bryan Vallejos (reservas, detalle_servicio)
**Pregunta:** ¿Por qué la reserva y sus detalles se guardan dentro de `transaction.atomic`?

**Respuesta:** Para que se guarde todo o nada. Si falla un detalle (por ejemplo, un servicio repetido), se deshace también la reserva y no queda una reserva a medias. La transacción se abre en la base de Oracle, que se obtiene con el router, y no en la SQLite por defecto.

### Bastián Saez (servicios_extra)
**Pregunta:** ¿Cómo sabe el repositorio de servicios si un servicio ya fue contratado, sin importar el modelo de Bryan?

**Respuesta:** Usa la relación inversa `detalles`, que declara el modelo de detalle_servicio con `related_name="detalles"`. Con `detalles__isnull=False` consulta si hay algún detalle asociado. Si lo hay, el caso de uso lanza `ServicioEnUsoError` y no deja eliminarlo. Así no hay un import cruzado entre los modelos.

## Pregunta común

**Pregunta:** ¿Por qué el caso de uso no importa el modelo de Django?

**Respuesta:** Por la regla de dependencia: la lógica de negocio no debe depender de detalles técnicos. El caso de uso recibe el puerto (la interfaz del repositorio) y no sabe si detrás hay Oracle, Django u otra cosa. Así se prueba sin base de datos y se puede cambiar la persistencia sin tocar la lógica.