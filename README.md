# Campus Tareas

Gestor de tareas académicas con JavaScript, Cloud Firestore y GitHub Pages.

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

## Configuración y despliegue

El proyecto de Firebase es `campus-tareas`, con Cloud Firestore Standard en `southamerica-west1` (Santiago), base `(default)` y autenticación anónima habilitada. Las reglas se publican desde la consola de Firestore utilizando `firestore.rules`.

El sitio se publica en **GitHub Pages** mediante `.github/workflows/deploy.yml`. En Settings → Pages, seleccionar GitHub Actions como origen. Al subir cambios a `main` se comprueba la sintaxis, se ejecutan las pruebas y, si pasan, se publica el contenido de `public/`. Las solicitudes de cambios ejecutan las comprobaciones sin publicar.

La configuración del SDK se encuentra en `public/firebase-config.json`. Son identificadores públicos de la app, no una clave privada de servicio. La protección de los documentos depende de Authentication y de las reglas de Firestore. No se utiliza el SDK Admin ni se requiere una clave de servicio en el repositorio. Para desplegar se usan los permisos temporales de GitHub Actions.

Para reproducir el proyecto con otra cuenta:

1. Crear un proyecto Firebase en plan Spark y registrar una app web.
2. Crear Cloud Firestore Standard en modo producción y habilitar Authentication → Anónimo.
3. Publicar las reglas de `firestore.rules`.
4. Reemplazar `public/firebase-config.json` por la configuración de esa app.
5. Crear un repositorio público, subir el código a `main` y seleccionar GitHub Actions en Settings → Pages.
6. Revisar los trabajos `check` y `deploy` y abrir la URL que entrega el workflow.

Para ejecutar la interfaz localmente:

```bash
python3 -m http.server 8000 --directory public
```

Abrir `http://localhost:8000`. Se conecta al proyecto real de Firestore. `firebase.json` y `.firebaserc` permiten usar Firebase CLI para mantener las reglas si se cuenta con autorización; el sitio web se aloja en GitHub Pages.

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

Las pruebas de interfaz y las comprobaciones de acceso ya ejecutadas se registran en [docs/verificacion.md](docs/verificacion.md).

## Publicaciones y entrega

- [Artículo de Antony en DEV.to](https://dev.to/antonys3010/una-aplicacion-de-tareas-academicas-con-javascript-y-cloud-firestore-40nf)
- [Artículo de Adriana en DEV.to](https://dev.to/antonys3010/de-un-commit-a-una-aplicacion-publicada-campus-tareas-con-firestore-g8f)
- [Video público de 4 minutos](https://www.youtube.com/watch?v=YAXXFRYB4Rk)
- [Aplicación publicada](https://antonys3010.github.io/campus-tareas-nosql/)
- [Enlaces para la entrega de Antony](docs/enlaces-antony.txt)

El artículo de Adriana está publicado desde la cuenta de Antony y señala expresamente su autoría al inicio. El mensaje para Telegram se encuentra en `docs/mensaje-telegram.txt`; todavía no se ha enviado al grupo.

## Referencias

- https://firebase.google.com/docs/firestore/data-model
- https://firebase.google.com/docs/firestore/security/rules-conditions
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://firebase.google.com/docs/web/alt-setup
- https://firebase.google.com/pricing
