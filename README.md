# Bosque Nativo – Reservas de cabañas (G08)

Backend con arquitectura hexagonal (Django 5.2, Oracle 26ai en FreeSQL, Django REST Framework) y frontend React + Vite.
Proyecto final de Back End, INACAP 2026.

**Equipo:** Carla Caro, Bryan Vallejos, Bastián Saez.

## Problema
Un complejo turístico arrienda cabañas por noche y ofrece servicios adicionales (tinaja, desayuno, leña) dentro de la reserva.
Entidades: `huespedes`, `cabanas`, `servicios_extra`, `reservas` (entidad principal) y `detalle_servicio`.

## Reglas de negocio (viven en los casos de uso, `application/`)
- **R1** Una cabaña no puede tener dos reservas no canceladas con fechas que se crucen.
- **R2** El número de personas no supera la capacidad de la cabaña.
- **R3** Total = noches × valor_noche + servicios; mínimo 2 noches.

Estados de la reserva: `pendiente → confirmada → finalizada` y `pendiente / confirmada → cancelada`.

## Roles
- **administrador:** todo.
- **recepcionista:** crea y confirma reservas; no cancela confirmadas ni cambia tarifas.

Usuarios de prueba por rol: *(se documentan en la semana 3)*

## Reporte
Ocupación por cabaña en un mes (noches ocupadas / noches del mes).

## Estructura del repositorio
```
BackEnd/     proyecto Django (bosque_nativo_project, app reservas) y sql/
frontend/    React + Vite (semana 6)
docs/        modelo_er.png, diccionario_datos.md, bitacora.md, anexo_a.md, capturas/
README.md
```

## Instalación desde cero
Requisitos: Python 3.12 o superior, Git y una cuenta en FreeSQL (Oracle 26ai).

1. **Tablas en Oracle.** En la hoja de trabajo de FreeSQL, ejecutar como script (F5), en este orden:
   `BackEnd/sql/01_crear_tablas.sql` y luego `BackEnd/sql/02_datos_ejemplo.sql`.
   Comprobar con `SELECT table_name FROM user_tables;` (deben salir 5 tablas).
2. **Entorno virtual** (desde la carpeta `BackEnd/`):
   ```
   python -m venv entorno
   .\entorno\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **Credenciales.** Copiar `BackEnd/.env.example` a `BackEnd/.env` y completar los valores propios
   (cada integrante usa su esquema de FreeSQL). `DB_SERVICE` lleva solo el nombre del servicio; `settings.py` arma la
   conexión «servidor:puerto/servicio» (Easy Connect). El `.env` nunca se sube al repositorio.
   Para generar la `SECRET_KEY`:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
4. **Probar la conexión a Oracle:**
   ```
   python manage.py check --database negocio
   ```
   Debe responder `System check identified no issues (0 silenced).`

## Dos bases de datos
- `default` (SQLite): tablas internas de Django (usuarios, grupos, sesiones, tokens).
- `negocio` (Oracle): solo las tablas del negocio. Un router envía allí los modelos de la app `reservas`.
  Los modelos usan `managed = False`: las tablas las crea el script SQL, no las migraciones.

## Avance por semana
- **Semana 1:** modelo de datos, diccionario, scripts SQL, repositorio, proyecto Django con dos bases y router, conexión a Oracle.

Seguimiento semanal: `docs/seguimiento_semanal.md` y `docs/Guia_Proyecto_Cabanas.xlsx`.
