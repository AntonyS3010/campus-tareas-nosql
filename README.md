# Campus Tareas

Gestor de tareas académicas con JavaScript, Cloud Firestore y Firebase Hosting.

**Integrantes:** Antony Piero Solorzano Zegarra y Adriana Rafaela Laos Gonzáles.

## Qué hace

Permite crear, consultar, editar, completar, filtrar y eliminar tareas. Cada tarea incluye un título y un curso. Los datos se guardan en Firestore; no hay un almacenamiento local alternativo que simule la base de datos.

La autenticación anónima asigna un identificador a cada visitante. Las reglas restringen las operaciones a las tareas de ese identificador. Cada navegador tiene su propio espacio: no es un tablero compartido entre los integrantes. Borrar los datos del navegador o cambiar de dispositivo impide recuperar esa sesión anónima. Para cuentas recuperables se necesitaría agregar inicio de sesión permanente.

## Estructura de datos

Ruta: `users/{uid}/tasks/{taskId}`.

```javascript
{
  title: "Preparar exposición de NoSQL",
  course: "Base de Datos II",
  done: false,
  createdAt: /* timestamp del servidor */
}
```

## Publicación inicial

1. Crear un repositorio **público** en GitHub llamado `campus-tareas-nosql`. Subir el contenido de esta carpeta a la raíz, incluyendo `.github/workflows/deploy.yml`, en la rama `main`. Agregar al otro integrante como colaborador.
2. Crear un proyecto en https://console.firebase.google.com/ con el plan Spark. Registrar una aplicación web. No activar Analytics, Storage, Functions ni App Hosting: para este proyecto se utiliza **Hosting**.
3. En Authentication → Sign-in method, habilitar **Anónimo**.
4. Crear la base de datos **Cloud Firestore, edición Standard, base `(default)`**, en modo producción. Elegir una ubicación disponible y registrar cuál se utilizó.
5. En Firestore → Reglas, copiar y publicar el contenido de `firestore.rules`. No utilizar reglas abiertas. La automatización incluida publica la app; las reglas se configuran por separado en este paso.
6. En el equipo con Node.js, instalar Firebase CLI y autorizar el proyecto:

```bash
npm install -g firebase-tools
firebase login
firebase use --add
```

Ejecutar los comandos desde esta carpeta; al solicitar un alias usar `default`. Esto genera `.firebaserc`, que puede subirse al repositorio porque solo identifica el proyecto.

7. Configurar la integración oficial:

```bash
firebase init hosting:github
```

Seleccionar el repositorio público. Si el asistente crea archivos adicionales de workflow, conservar un solo flujo de publicación. El proyecto incluye `.github/workflows/deploy.yml`. Renombrar el secreto creado por la CLI a `FIREBASE_SERVICE_ACCOUNT`, o cambiar la referencia en ese archivo al nombre real. No pegar la clave de servicio en archivos del repositorio ni en el artículo.

8. En GitHub → Settings → Secrets and variables → Actions → Variables, agregar `FIREBASE_PROJECT_ID` con el ID exacto del proyecto. Mantener la credencial de servicio como **Secret**, no como Variable.
9. Subir los cambios a `main`. Abrir Actions y esperar que terminen los trabajos `check` y `deploy`. Abrir la URL que devuelve Firebase Hosting.

La app obtiene la configuración pública desde `/__/firebase/init.json`, que sirve Firebase Hosting. Un servidor HTTP genérico no proporciona esa ruta. Para vista local conectada al mismo proyecto se puede usar `firebase emulators:start --only hosting`; los servicios de datos siguen siendo los del proyecto real. No se incluyen emuladores de Auth/Firestore.

## Comprobaciones

```bash
npm run check
npm test
```

Estas comprobaciones revisan la sintaxis y la validación del formulario. No sustituyen pruebas de reglas de seguridad ni una prueba de integración contra Firebase.

Antes de entregar, comprobar en la app publicada:

- Crear una tarea y ver su documento en Firestore.
- Recargar y comprobar que continúa disponible.
- Editarla, completarla y probar los filtros.
- Abrir una ventana privada y comprobar que no aparecen las tareas del otro navegador.
- Eliminar la tarea y comprobar que desaparece de Firestore.
- Hacer un cambio visible en el texto del sitio, subirlo a `main` y registrar el workflow exitoso y el cambio publicado.
- Verificar reglas con el simulador de Firestore: usuario propietario autorizado; usuario diferente y visitante sin autenticar rechazados. Probar también tipos incorrectos y campos adicionales.

## Entrega académica

Los textos de `docs/` son versiones de trabajo que deben completarse con los enlaces y las capturas reales. Publicar un artículo en cada cuenta personal. El video puede mostrar a ambos integrantes; confirmar con el docente si además exige uno por integrante. Publicarlo con visibilidad pública y duración inferior a cinco minutos.

El ZIP de preparación contiene el proyecto. El ZIP final solicitado por el docente debe prepararse después de publicar, con los enlaces reales a ambos artículos, el video, el repositorio y la app. No entregar un archivo con campos pendientes.

## Referencias

- https://firebase.google.com/docs/firestore/data-model
- https://firebase.google.com/docs/firestore/security/rules-conditions
- https://firebase.google.com/docs/hosting/github-integration
- https://firebase.google.com/docs/web/alt-setup
- https://firebase.google.com/pricing
