# Verificación de Campus Tareas

Fecha: 14 de noviembre de 2026 (Perú).

## Publicación

- Repositorio: https://github.com/AntonyS3010/campus-tareas-nosql
- App: https://antonys3010.github.io/campus-tareas-nosql/
- Despliegue: https://github.com/AntonyS3010/campus-tareas-nosql/actions/runs/43671790256
- Resultado: check, package y deploy terminaron correctamente.

## Prueba de interfaz

En la web publicada se creó una tarea, se editó su título, se completó, se recargó la página y se comprobó que el título y estado seguían disponibles. Se probaron los filtros Pendientes y Completadas. La tarea de prueba se eliminó y la lista quedó vacía.

## Pruebas contra Firebase

Las solicitudes se ejecutaron con dos cuentas anónimas creadas exclusivamente para esta comprobación. Los documentos y las dos cuentas de prueba se limpiaron al finalizar. No se almacenaron tokens en este informe.

| Prueba | HTTP recibido | Resultado |
| --- | --- | --- |
| Autenticación anónima 1 | 200 | Correcto |
| Autenticación anónima 2 | 200 | Correcto |
| Crear documento propio con fecha del servidor | 200 | Correcto |
| Leer documento propio | 200 | Correcto |
| Rechazar lectura de otro usuario | 403 | Correcto |
| Rechazar lectura sin autenticar | 403 | Correcto |
| Actualizar estado propio | 200 | Correcto |
| Rechazar modificación de otro usuario | 403 | Correcto |
| Rechazar tipo incorrecto | 403 | Correcto |
| Rechazar campos adicionales | 403 | Correcto |
| Rechazar cambio de fecha original | 403 | Correcto |
| Rechazar eliminación de otro usuario | 403 | Correcto |
| Eliminar documento propio de prueba | 200 | Correcto |
| Confirmar eliminación del documento | 404 | Correcto |
| Limpiar cuenta anónima de prueba | 200 | Correcto |
| Limpiar cuenta anónima de prueba | 200 | Correcto |

## Alcances

Las comprobaciones cubren las operaciones básicas y las condiciones de acceso enumeradas. No incluyen una auditoría completa, pruebas de carga, recuperación de cuentas ni protección contra abuso mediante App Check. La autenticación es anónima y depende de conservar la sesión del navegador.

## Video

Se preparó un recorrido de 4 minutos, 1920 × 1080, con explicaciones en pantalla y capturas de la aplicación publicada. Sin narración. Video público: https://www.youtube.com/watch?v=YAXXFRYB4Rk

Artículo de Antony: https://dev.to/antonys3010/una-aplicacion-de-tareas-academicas-con-javascript-y-cloud-firestore-40nf
