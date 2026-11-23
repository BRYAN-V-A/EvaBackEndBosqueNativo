# Cabañas «Bosque Nativo» · API de reservas

Proyecto Final de Back End (INACAP): API hexagonal con Django, Oracle (FreeSQL) y React.
Grupo G08 · Reservas de cabañas con servicios adicionales (tinaja, desayuno, leña).

## Integrantes y entidades a cargo

| Integrante      | Entidades                             |
|-----------------|---------------------------------------|
| Carla Caro      | huespedes, cabanas                    |
| Bryan Vallejos  | reservas, detalle_servicio            |
| Bastián Saez    | servicios_extra, reporte de ocupación,| 
|                 |panel de administración                |

## Requisitos

- Python 3.12 o superior (con `python.exe` en el PATH)
- Visual Studio Code
- GitHub Desktop
- Una cuenta en [freesql.com](https://freesql.com) (cada integrante usa su propio esquema)
- Postman
- Node.js 20 o superior (solo para el frontend)

## Instalación (backEnd)

1. Clonar el repositorio y abrir la carpeta en Visual Studio Code.
2. Crear y activar el entorno virtual:
   ```
   python -m venv entorno
   .\entorno\Scripts\Activate.ps1
   ```
3. Entrar a la carpeta del proyecto e instalar dependencias:
   ```
   cd BackEnd
   pip install -r requirements.txt
   ```
4. Crear las tablas en TU esquema de FreeSQL ejecutando como script, en este orden:
   `sql/01_crear_tablas.sql` y `sql/02_datos_ejemplo.sql`.
5. Copiar `.env.example` a `.env` y completarlo con los datos de TU esquema
   (host, servicio, usuario y contraseña de FreeSQL, más una SECRET_KEY propia).
   El archivo `.env` nunca se sube al repositorio.
6. Probar la conexión a Oracle (desde `BackEnd`):
   ```
   python manage.py check
   python manage.py shell -c "from django.db import connections; connections['negocio'].ensure_connection(); print('Conexion a Oracle OK')"
   ```
   Debe responder `Conexion a Oracle OK`.

La conexión a Oracle usa el formato `host:puerto/servicio` dentro de `NAME`
(ver `bosque_nativo_project/settings.py`); `HOST` y `PORT` quedan vacíos.

## Estructura del repositorio

```
BackEnd/     proyecto Django (bosque_nativo_project), app reservas y carpeta sql/
frontend/    React + Vite (semana 6)
docs/        modelo ER, diccionario de datos, bitácora, colección de Postman, capturas
```

## Arquitectura hexagonal (app `reservas`)

```
reservas/
  domain/            núcleo: sin Django ni base de datos
    entities/          una entidad (dataclass) por tabla
    repositories/      puertos: interfaces abstractas de cada repositorio
  application/       lógica de negocio
    exceptions.py      excepciones de negocio
    use_cases/         casos de uso (reciben el puerto por constructor)
  infrastructure/    detalles técnicos
    models/            modelos de Django (managed = False, tablas ya creadas en Oracle)
    repositories/      adaptadores: implementan los puertos con Django ORM
    di.py              contenedor simple que entrega cada repositorio
  adaptadores/       serializers y vistas de la API (semana 5)
```

**Regla de dependencia:** las dependencias apuntan hacia adentro.
`infrastructure` conoce a `application` y `domain`; `application` solo conoce a `domain`;
`domain` no importa nada de Django ni de las otras capas.

Hay dos bases de datos: `default` (SQLite, tablas internas de Django: usuarios, tokens)
y `negocio` (Oracle, tablas del negocio). Un router (`routers.py`) decide a cuál va cada modelo.

## Reglas de negocio

- **R1:** una cabaña no puede tener dos reservas no canceladas con fechas que se crucen.
- **R2:** el número de personas no supera la capacidad de la cabaña.
- **R3:** total = noches × valor_noche + servicios; mínimo 2 noches.

Estados de la reserva: pendiente → confirmada → finalizada · pendiente o confirmada → cancelada.

## Probar las capas (semana 2)

Cada integrante tiene su propio script de comprobación en la carpeta `BackEnd`.
Se ejecutan desde `BackEnd`, con el entorno activado:

| Integrante      | Entidades que prueba       | Comando                                                                              |
|-----------------|----------------------------|--------------------------------------------------------------------------------------|
| Carla Caro      | huespedes, cabanas         | `python manage.py shell -c "exec(open('probar_capas.py', encoding='utf-8').read())"` |
| Bryan Vallejos | reservas, detalle_servicio | `python manage.py shell -c "exec(open('probar_capas_bryan.py', encoding='utf-8').read())"` |
| Bastián Saez    | servicios_extra            | `python manage.py shell -c "exec(open('probar_capas_bastian.py', encoding='utf-8').read())"` |

Cada script crea datos de prueba, comprueba duplicados, validaciones y reglas de su entidad,
y borra lo que creó, así que la base queda igual que antes.

## Usuarios de prueba

(Se completan en la semana 3, cuando existan los roles administrador y recepcionista.)

## Avance por semana

- **Semana 1:** modelo ER, diccionario de datos, scripts SQL, repositorio, proyecto Django y conexión a Oracle.
- **Semana 2:** capas hexagonales de las entidades maestras (huespedes, cabanas y servicios_extra) y modelos de reservas y detalle_servicio: dominio, puertos, excepciones, casos de uso CRUD, modelos y repositorios, contenedor de dependencias y un script de comprobación por integrante.