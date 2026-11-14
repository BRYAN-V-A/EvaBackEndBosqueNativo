-- Cabañas «Bosque Nativo» · datos de ejemplo.
-- Ejecutar DESPUES de 01_crear_tablas.sql y una sola vez (si lo repiten, fallan los UNIQUE).
-- Para empezar de cero, vuelvan a correr 01 y luego este.

-- Huespedes (rut chileno o pasaporte)
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('15234567-4', 'Camila Reyes Fuentes', 'camila.reyes@correo.cl', 'Chile');
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('17890123-0', 'Matías Soto Araya', 'matias.soto@correo.cl', 'Chile');
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('9876543-3', 'Patricia Navarro Vega', NULL, 'Chile');
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('AAB123456', 'Lucía Fernández Gómez', 'lucia.fernandez@mail.com', 'Argentina');
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('C01X00T47', 'Thomas Müller Becker', 'thomas.mueller@mail.de', 'Alemania');
INSERT INTO huespedes (documento, nombre, email, pais) VALUES ('18456789-K', 'Javiera Pizarro Lagos', 'javiera.pizarro@correo.cl', 'Chile');

-- Cabañas (la ultima esta fuera de servicio: activa = 0)
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-01', 'Cabaña Alerce', 4, 65000, 1);
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-02', 'Cabaña Coihue', 2, 48000, 1);
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-03', 'Cabaña Ulmo', 6, 89000, 1);
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-04', 'Cabaña Canelo', 4, 70000, 1);
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-05', 'Cabaña Lenga', 8, 120000, 1);
INSERT INTO cabanas (codigo, nombre, capacidad, valor_noche, activa) VALUES ('CAB-06', 'Cabaña Quila', 2, 45000, 0);

-- Servicios extra
INSERT INTO servicios_extra (nombre, precio) VALUES ('Tinaja caliente', 35000);
INSERT INTO servicios_extra (nombre, precio) VALUES ('Desayuno campestre', 8500);
INSERT INTO servicios_extra (nombre, precio) VALUES ('Leña (atado)', 6000);
INSERT INTO servicios_extra (nombre, precio) VALUES ('Cabalgata guiada', 25000);
INSERT INTO servicios_extra (nombre, precio) VALUES ('Cena de bienvenida', 18000);

-- Reservas de ejemplo (respetan R1, R2 y R3). total = noches x valor_noche + servicios.
-- 1) Camila, CAB-01, 3 noches, 3 personas: 3 x 65.000 + tinaja 35.000 + 2 lena 12.000 = 242.000
INSERT INTO reservas (id_huesped, id_cabana, fecha_llegada, fecha_salida, n_personas, total, estado)
VALUES ((SELECT id_huesped FROM huespedes WHERE documento = '15234567-4'),
        (SELECT id_cabana FROM cabanas WHERE codigo = 'CAB-01'),
        DATE '2026-12-20', DATE '2026-12-23', 3, 242000, 'confirmada');

-- 2) Thomas, CAB-03, 4 noches, 5 personas: 4 x 89.000 + 8 desayunos 68.000 + 2 cabalgatas 50.000 = 474.000
INSERT INTO reservas (id_huesped, id_cabana, fecha_llegada, fecha_salida, n_personas, total, estado)
VALUES ((SELECT id_huesped FROM huespedes WHERE documento = 'C01X00T47'),
        (SELECT id_cabana FROM cabanas WHERE codigo = 'CAB-03'),
        DATE '2026-12-26', DATE '2026-12-30', 5, 474000, 'pendiente');

-- 3) Matias, CAB-02, 3 noches, 2 personas: 3 x 48.000 + 2 desayunos 17.000 = 161.000
INSERT INTO reservas (id_huesped, id_cabana, fecha_llegada, fecha_salida, n_personas, total, estado)
VALUES ((SELECT id_huesped FROM huespedes WHERE documento = '17890123-0'),
        (SELECT id_cabana FROM cabanas WHERE codigo = 'CAB-02'),
        DATE '2026-11-06', DATE '2026-11-09', 2, 161000, 'finalizada');

-- 4) Lucia, CAB-01, 2 noches, 2 personas, cancelada y sin servicios: 2 x 65.000 = 130.000
INSERT INTO reservas (id_huesped, id_cabana, fecha_llegada, fecha_salida, n_personas, total, estado)
VALUES ((SELECT id_huesped FROM huespedes WHERE documento = 'AAB123456'),
        (SELECT id_cabana FROM cabanas WHERE codigo = 'CAB-01'),
        DATE '2026-12-28', DATE '2026-12-30', 2, 130000, 'cancelada');

-- Detalle de servicios (cada reserva se identifica por su fecha de llegada, unica en estos datos)
INSERT INTO detalle_servicio (id_reserva, id_servicio, cantidad, precio_unitario)
SELECT r.id_reserva, s.id_servicio, 1, s.precio FROM reservas r, servicios_extra s
WHERE r.fecha_llegada = DATE '2026-12-20' AND s.nombre = 'Tinaja caliente';
INSERT INTO detalle_servicio (id_reserva, id_servicio, cantidad, precio_unitario)
SELECT r.id_reserva, s.id_servicio, 2, s.precio FROM reservas r, servicios_extra s
WHERE r.fecha_llegada = DATE '2026-12-20' AND s.nombre = 'Leña (atado)';
INSERT INTO detalle_servicio (id_reserva, id_servicio, cantidad, precio_unitario)
SELECT r.id_reserva, s.id_servicio, 8, s.precio FROM reservas r, servicios_extra s
WHERE r.fecha_llegada = DATE '2026-12-26' AND s.nombre = 'Desayuno campestre';
INSERT INTO detalle_servicio (id_reserva, id_servicio, cantidad, precio_unitario)
SELECT r.id_reserva, s.id_servicio, 2, s.precio FROM reservas r, servicios_extra s
WHERE r.fecha_llegada = DATE '2026-12-26' AND s.nombre = 'Cabalgata guiada';
INSERT INTO detalle_servicio (id_reserva, id_servicio, cantidad, precio_unitario)
SELECT r.id_reserva, s.id_servicio, 2, s.precio FROM reservas r, servicios_extra s
WHERE r.fecha_llegada = DATE '2026-11-06' AND s.nombre = 'Desayuno campestre';

COMMIT;
