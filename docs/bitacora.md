# Bitácora · Cabañas «Bosque Nativo» (G08)

Una entrada por semana y por integrante. Debe coincidir con los commits del repositorio.
Si se usó IA, anotar qué se le preguntó y qué se cambió del resultado.

## Semana 1 · Diseño, base de datos y conexión

### Carla Caro
### Carla Caro
- **Qué hice:** Preparé mi computador (Python, VS Code, GitHub Desktop), cloné el repositorio, creé el entorno virtual y mi .env. Borré las tablas de la actividad anterior de mi esquema de FreeSQL, ejecuté los scripts sql/01_crear_tablas.sql y sql/02_datos_ejemplo.sql, y comprobé en user_tables que quedaron las 5 tablas y que el subtotal de detalle_servicio se calcula bien. Probé la conexión desde Django. En el reparto me quedé con huespedes y cabanas.
- **En qué archivos:** docs/modelo_er.png, docs/diccionario_datos.md, docs/seguimiento_semanal.md, docs/Guia_Proyecto_Cabanas.xlsx, docs/capturas/user_tables_carla.png, sql/01_crear_tablas.sql, sql/02_datos_ejemplo.sql, BackEnd/bosque_nativo_project/settings.py.
- **Problema que tuve y cómo lo resolví:** Al probar la conexión con Django me dio DPY-6003 (SID "26ai_un3c1" no registrado). Con HOST y PORT separados en settings.py, Django usa NAME como SID. Lo corregí dejando HOST y PORT vacíos y poniendo "servidor:puerto/servicio" (Easy Connect) en NAME. Después la conexión funcionó.
- **Qué haré la semana siguiente:** Programar las capas hexagonales de huespedes y cabanas: entidad de dominio, puerto, excepciones, casos de uso CRUD, modelo con managed = False y repositorio.
- **Uso de IA (qué pregunté y qué cambié):** Usé Claude para armar el modelo ER, el diccionario de datos, los scripts SQL, la guía de seguimiento en Excel y el README, y para diagnosticar el error DPY-6003. **Qué cambié o revisé yo:** Verifiqué por mi cuenta el resultado de lo que generó la IA. Ejecuté los scripts SQL en mi esquema de FreeSQL y comprobé que se crearon las 5 tablas y que el subtotal virtual de detalle_servicio se calcula correctamente. Probé la conexión de Django con Oracle y, al aparecer el error DPY-6003, apliqué la corrección en settings.py y confirmé que la conexión funcionaba. Además, limpié mi esquema de las tablas de la actividad anterior, configuré mi propio .env con mis credenciales y organicé las carpetas docs/ y sql/ del repositorio.

### Brayan Vallejos
- **Qué hice:**
- **En qué archivos:**
- **Problema que tuve y cómo lo resolví:**
- **Qué haré la semana siguiente:**
- **Uso de IA (qué pregunté y qué cambié):**

### Bastián Saez
- **Qué hice:**
- **En qué archivos:**
- **Problema que tuve y cómo lo resolví:**
- **Qué haré la semana siguiente:**
- **Uso de IA (qué pregunté y qué cambié):**

## Semana 2 · Capas hexagonales de las entidades maestras
