# Una aplicación de tareas académicas con JavaScript y Cloud Firestore

**Autor:** Antony Piero Solorzano Zegarra  
**Proyecto desarrollado con:** Adriana Rafaela Laos Gonzáles

## El problema y el alcance

Entre clases, prácticas y exposiciones, las entregas pueden quedar repartidas en distintos lugares. Campus Tareas reúne los pendientes en una página: cada tarea tiene un título, un curso y un estado. El alcance es pequeño para poder explicar el recorrido completo de un dato, desde el formulario hasta su almacenamiento en la nube.

La interfaz está construida con HTML, CSS y JavaScript. Cloud Firestore almacena los datos y GitHub Pages sirve los archivos de la aplicación.

## Cómo se organiza la información

Firestore es una base de datos NoSQL orientada a documentos. En este proyecto cada tarea es un documento dentro de `users/{uid}/tasks`. Sus campos son `title`, `course`, `done` y `createdAt`.

La aplicación utiliza las operaciones `addDoc`, `updateDoc` y `deleteDoc`. Para leer las tareas registra una suscripción con `onSnapshot`, ordenada por fecha de creación. La interfaz recibe las actualizaciones sin tener que consultar manualmente después de cada operación.

El formulario elimina los espacios al inicio y al final y limita la longitud del título y del curso. Los textos se insertan en la página mediante `textContent`.

## Acceso a los datos

Cada visitante entra mediante autenticación anónima. Las reglas comprueban que su identificador coincida con el de la ruta del documento y validan los campos permitidos. La fecha de creación se asigna desde el servidor y no puede modificarse en una actualización.

Esta decisión simplifica la demostración, aunque tiene una limitación: las tareas pertenecen a la sesión del navegador. No existe recuperación de cuenta si se borra esa sesión.

## Del repositorio a la nube

El repositorio incluye un workflow de GitHub Actions. En una solicitud de cambios se ejecutan las comprobaciones de sintaxis y las pruebas de validación. Cuando los cambios llegan a `main`, y esas comprobaciones pasan, se ejecuta la publicación en GitHub Pages.

La publicación utiliza permisos temporales de GitHub Actions y no requiere una clave privada de Firebase. Las reglas de Firestore se publican por separado durante la configuración inicial.

## Configuración del proyecto

El proyecto de Firebase se llama `campus-tareas`. La base `(default)` usa Firestore Standard en `southamerica-west1`, la región de Santiago. Se habilitó el proveedor Anónimo en Authentication y se publicaron las reglas de `firestore.rules`.

En el frontend, `firebase-config.json` contiene los identificadores públicos de la aplicación. El código carga ese archivo e inicializa el SDK. La configuración pública no sustituye los permisos: las reglas de Firestore son las que deciden si una operación se acepta.

Para reproducir el proyecto, se registra una app web en Firebase, se habilitan los servicios anteriores y se reemplaza el archivo de configuración. En el repositorio público, Settings → Pages debe usar GitHub Actions como origen. El workflow publica la carpeta `public/`.

## Comprobaciones de funcionamiento

En la aplicación publicada se creó la tarea «Preparar exposición de NoSQL», del curso Base de Datos II. Se editó el título a «Preparar exposición y demo de NoSQL», se marcó como completada y se recargó la página. La tarea conservó el título y el estado. Después se eliminó y el contador volvió a cero.

Además de las dos pruebas locales de validación, se comprobaron las reglas mediante solicitudes reales a Firebase. La lectura propia se aceptó; la lectura sin autenticación y la lectura con otra cuenta recibieron HTTP 403. También se rechazaron las modificaciones y eliminaciones desde otra cuenta, los campos adicionales, un estado con tipo incorrecto y el cambio de la fecha de creación. Los documentos y las cuentas creados para esas pruebas se limpiaron al terminar.

La [ejecución de despliegue](https://github.com/AntonyS3010/campus-tareas-nosql/actions/runs/43671790256) terminó con `check`, `package` y `deploy` correctos. Estas comprobaciones cubren el flujo básico y las reglas indicadas; no son una auditoría completa de seguridad.

## Código y demostración

- [Repositorio público](https://github.com/AntonyS3010/campus-tareas-nosql)
- [Aplicación publicada](https://antonys3010.github.io/campus-tareas-nosql/)
- Video público: PENDIENTE

Referencias: [modelo de datos de Firestore](https://firebase.google.com/docs/firestore/data-model), [reglas de seguridad](https://firebase.google.com/docs/firestore/security/rules-conditions) e [integración con GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
