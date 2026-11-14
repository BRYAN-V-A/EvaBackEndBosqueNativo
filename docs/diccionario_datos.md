# Diccionario de datos · Cabañas «Bosque Nativo»

Base de datos: Oracle 26ai (FreeSQL). Una tabla por entidad. Las claves se identifican con **PK** (primaria), **FK** (foránea) y **UQ** (única).

## huespedes
Personas que reservan (chilenos con rut o extranjeros con pasaporte).

| Columna | Tipo Oracle | Nulo | Restricción | Descripción |
|---|---|---|---|---|
| id_huesped | NUMBER(11) IDENTITY | No | PK `pk_huespedes` | Identificador autogenerado |
| documento | VARCHAR2(20) | No | UQ `uq_huespedes_documento` | Rut o pasaporte del huésped |
| nombre | VARCHAR2(100) | No | | Nombre completo |
| email | VARCHAR2(100) | Sí | | Correo de contacto |
| pais | VARCHAR2(60) | No | | País de origen |

## cabanas
Cabañas que se arriendan por noche.

| Columna | Tipo Oracle | Nulo | Restricción | Descripción |
|---|---|---|---|---|
| id_cabana | NUMBER(11) IDENTITY | No | PK `pk_cabanas` | Identificador autogenerado |
| codigo | VARCHAR2(20) | No | UQ `uq_cabanas_codigo` | Código interno de la cabaña (ej. CAB-01) |
| nombre | VARCHAR2(100) | No | | Nombre de la cabaña |
| capacidad | NUMBER(3) | No | CHECK `ck_cabanas_capacidad` (> 0) | Máximo de personas |
| valor_noche | NUMBER(10,2) | No | CHECK `ck_cabanas_valor` (>= 0) | Tarifa por noche |
| activa | NUMBER(1) | No | DEFAULT 1, CHECK `ck_cabanas_activa` (0 o 1) | 1 = disponible para reservar, 0 = no |

## servicios_extra
Servicios adicionales que se contratan dentro de la reserva (tinaja, desayuno, leña).

| Columna | Tipo Oracle | Nulo | Restricción | Descripción |
|---|---|---|---|---|
| id_servicio | NUMBER(11) IDENTITY | No | PK `pk_servicios_extra` | Identificador autogenerado |
| nombre | VARCHAR2(60) | No | UQ `uq_servicios_nombre` | Nombre del servicio |
| precio | NUMBER(10,2) | No | CHECK `ck_servicios_precio` (>= 0) | Precio por unidad |

## reservas (entidad principal)
Estadía de un huésped en una cabaña.

| Columna | Tipo Oracle | Nulo | Restricción | Descripción |
|---|---|---|---|---|
| id_reserva | NUMBER(11) IDENTITY | No | PK `pk_reservas` | Identificador autogenerado |
| id_huesped | NUMBER(11) | No | FK `fk_reservas_huesped` → huespedes | Quién reserva |
| id_cabana | NUMBER(11) | No | FK `fk_reservas_cabana` → cabanas | Cabaña reservada |
| fecha_llegada | DATE | No | | Primer día de la estadía |
| fecha_salida | DATE | No | CHECK `ck_reservas_fechas` (salida > llegada) | Día de salida |
| n_personas | NUMBER(3) | No | CHECK `ck_reservas_personas` (> 0) | Personas que se alojan |
| total | NUMBER(12,2) | No | DEFAULT 0 | Total calculado: noches × valor_noche + servicios |
| estado | VARCHAR2(10) | No | DEFAULT 'pendiente', CHECK `ck_reservas_estado` (pendiente, confirmada, finalizada, cancelada) | Estado de la reserva |

Índices en las claves foráneas: `ix_reservas_huesped` e `ix_reservas_cabana`.

## detalle_servicio
Servicios contratados en cada reserva. Sin id propio: la clave es la pareja (id_reserva, id_servicio).

| Columna | Tipo Oracle | Nulo | Restricción | Descripción |
|---|---|---|---|---|
| id_reserva | NUMBER(11) | No | PK compuesta `pk_detalle_servicio`, FK `fk_detalle_reserva` → reservas (ON DELETE CASCADE) | Reserva a la que pertenece |
| id_servicio | NUMBER(11) | No | PK compuesta, FK `fk_detalle_servicio` → servicios_extra | Servicio contratado |
| cantidad | NUMBER(11) | No | CHECK `ck_detalle_cantidad` (> 0) | Unidades contratadas |
| precio_unitario | NUMBER(10,2) | No | | Precio del servicio al momento de reservar |
| subtotal | NUMBER(12,2) | — | Columna **virtual**: cantidad × precio_unitario | La calcula Oracle al leerla |

Índice en la clave foránea: `ix_detalle_servicio`.

## Resumen de restricciones (mínimos del proyecto)

- **Claves foráneas (mínimo 3):** 4 (fk_reservas_huesped, fk_reservas_cabana, fk_detalle_reserva, fk_detalle_servicio).
- **UNIQUE (mínimo 2):** 3 (documento, código de cabaña, nombre de servicio).
- **CHECK (mínimo 3):** 8 (capacidad, valor_noche, activa, precio, fechas, n_personas, estado, cantidad).
- **Clave primaria compuesta:** detalle_servicio (id_reserva, id_servicio).
- **Columna virtual:** detalle_servicio.subtotal.

## Reglas que NO van en Oracle (van en los casos de uso, capa application)

- **R1:** una cabaña no puede tener dos reservas no canceladas con fechas que se crucen (compara filas entre sí, un CHECK no puede hacerlo).
- **R2:** n_personas no supera la capacidad de la cabaña (compara con otra tabla).
- **R3:** mínimo de 2 noches y total = noches × valor_noche + servicios.
- Transiciones de estado permitidas: pendiente → confirmada → finalizada; pendiente o confirmada → cancelada.
