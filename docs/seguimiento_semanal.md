# Seguimiento semanal del proyecto

El avance del proyecto se sigue en el archivo **`Guia_Proyecto_Cabanas.xlsx`** (en esta misma carpeta).
Se generó con ayuda de IA (Claude) a partir del PDF «Proyecto Final de Back End» y se adaptó al problema
de nuestro grupo: G08 · Cabañas «Bosque Nativo».

## Qué contiene

| Hoja | Para qué sirve |
|---|---|
| **Checklist** | Un avance por fila, ordenado por semana (S1 a S7). Cada fila tiene una casilla ✔, el detalle de qué hacer en nuestro proyecto, el responsable y la referencia al PDF. Muestra cuántos avances lleva cada semana y el total. |
| **Pruebas Postman** | Las 17 pruebas mínimas del Anexo B del PDF, adaptadas a cabañas, con el resultado esperado de cada una. Se usa en la semana 5. |
| **Nuestro proyecto** | Resumen del problema: entidades, estados de la reserva, reglas R1 a R3, roles, reporte y entregas. |

## Cómo se usa

1. En la hoja Checklist, hacer clic en la celda de la columna ✔ y elegir ✔ en la lista desplegable cuando el avance esté terminado (Supr para quitarlo).
2. En la columna «Quién» elegir al responsable (Carla, Brayan, Bastián o Todos).
3. Antes de cada revisión del lunes, comparar el Checklist con el repositorio: un avance solo se marca cuando está subido a `main` y funciona.
4. El archivo es binario, así que git no puede mezclar cambios de dos personas. Lo actualiza una persona a la vez (hacer `git pull` antes de editarlo y subirlo de inmediato).

## Resumen de las semanas

| Semana | Tema | Nota | Cierre |
|---|---|---|---|
| 1 | Diseño, base de datos y conexión | Nota 1 · 2.1.1 | Modelo ER, diccionario, scripts SQL, repositorio, proyecto Django y conexión a Oracle |
| 2 | Capas hexagonales de las entidades maestras | Nota 1 · 2.1.3 | Dominio, puertos, excepciones, casos de uso, modelos y repositorios de huespedes, cabanas y servicios_extra |
| 3 | Entidad principal, reglas de negocio y seguridad | Nota 1 · 2.1.3 · 2.1.4 | Reserva con detalle en una transacción, R1 a R3, panel de administración, roles, login y logout |
| 4 | Revisión del backEnd terminado | **Nota 1** | Etiqueta `nota1`, README, capturas y defensa individual |
| 5 | API RESTful completa | Nota 2 · 3.1.1 a 3.1.4 | DRF, serializers, rutas, códigos HTTP, reporte y colección de Postman |
| 6 | Frontend React + Vite | Nota 2 · 3.1.2 · 3.1.4 | Login, mantenciones, reserva con detalle, reporte y mensajes de error |
| 7 | Demostración final y defensa | **Nota 2** | Etiqueta `nota2`, demostración completa y defensa individual |

Cada lunes (semanas 1 a 6) el último commit debe estar en `main` antes de las 08:30, con la bitácora (`docs/bitacora.md`) al día.
