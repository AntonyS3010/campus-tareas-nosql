# De un commit a una aplicación publicada: Campus Tareas con Firestore

**Autora:** Adriana Rafaela Laos Gonzáles  
**Proyecto desarrollado con:** Antony Piero Solorzano Zegarra

> Versión de trabajo. Completar los enlaces, las capturas y los resultados reales antes de publicar. Retirar este aviso al finalizar la revisión.

## Una aplicación pequeña para mostrar el proceso completo

Campus Tareas permite registrar pendientes por curso, editarlos, marcarlos como completados y eliminarlos. La aplicación utiliza JavaScript en el navegador, Cloud Firestore como base NoSQL y GitHub Pages para su publicación.

El propósito del proyecto es conectar esas piezas con un proceso repetible: que un cambio en el código pueda comprobarse y publicarse desde el repositorio.

## Construcción y persistencia

El formulario recoge el título de la tarea y el curso. Después de validar esos valores, el código crea un documento en Firestore. Las tareas se organizan en `users/{uid}/tasks/{taskId}` e incluyen un estado booleano y una fecha asignada por el servidor.

La lectura utiliza `onSnapshot`, por lo que la lista se actualiza cuando cambian los documentos. Editar una tarea modifica su documento; eliminarla retira ese registro de la colección. El almacenamiento no depende de una lista simulada en el navegador.

Cada visitante recibe una identidad anónima. Las reglas permiten acceder únicamente a la ruta asociada a esa identidad y rechazan documentos con campos o tipos que no correspondan al modelo. Esta separación no convierte el proyecto en una aplicación con cuentas recuperables: cambiar de navegador crea otro espacio.

## Qué automatiza el repositorio

El workflow tiene dos trabajos. El primero comprueba la sintaxis del código y ejecuta pruebas sobre las entradas del formulario. El segundo depende del primero y publica en GitHub Pages cuando la rama es `main`.

Las solicitudes de cambios ejecutan las comprobaciones, pero no publican en producción. Esto permite revisar una modificación antes de integrarla.

La configuración pública de Firebase queda en un archivo de la aplicación. El despliegue utiliza permisos temporales de GitHub Actions. La configuración inicial también requiere habilitar la autenticación anónima, crear Firestore y publicar sus reglas.

## Cómo comprobar la publicación

Una prueba útil consiste en cambiar una frase visible de la interfaz, subir el cambio y revisar el workflow. Después se abre la URL pública para comprobar que aparece la nueva frase. La marca verde de Actions debe acompañarse de la revisión del sitio y de sus operaciones contra Firestore.

Agregar aquí el enlace a la ejecución real, una captura de la aplicación y el resultado de crear y recuperar una tarea después de recargar. También registrar la comprobación de aislamiento entre dos sesiones.

## Alcances y siguientes pasos

El proyecto cubre un CRUD individual y un despliegue automático. Un siguiente paso posible sería incorporar cuentas permanentes para recuperar tareas desde distintos dispositivos. Para una publicación de mayor alcance también haría falta ampliar las pruebas de seguridad y revisar el uso de las cuotas del servicio.

## Enlaces

- Repositorio público: PENDIENTE
- Aplicación: PENDIENTE
- Video público: PENDIENTE

Referencias: [GitHub Pages y GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Firestore](https://firebase.google.com/docs/firestore/data-model) y [reglas de acceso](https://firebase.google.com/docs/firestore/security/rules-conditions).
