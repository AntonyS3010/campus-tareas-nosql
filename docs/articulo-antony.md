# Una aplicación de tareas académicas con JavaScript y Cloud Firestore

**Autor:** Antony Piero Solorzano Zegarra  
**Proyecto desarrollado con:** Adriana Rafaela Laos Gonzáles

> Versión de trabajo. Antes de publicar, agregar los enlaces, las capturas y el resultado del despliegue verificado. Este aviso se retira al completar esos pasos.

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

## Evidencias de funcionamiento

Antes de publicar este artículo, agregar una captura del documento creado en Firestore, una del workflow exitoso y una de la aplicación publicada. Registrar aquí el resultado real de crear, editar, recargar y eliminar una tarea. Las pruebas locales de validación no demuestran por sí solas la conexión con la nube.

## Código y demostración

- Repositorio público: PENDIENTE
- Aplicación: PENDIENTE
- Video público: PENDIENTE

Referencias: [modelo de datos de Firestore](https://firebase.google.com/docs/firestore/data-model), [reglas de seguridad](https://firebase.google.com/docs/firestore/security/rules-conditions) e [integración con GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
