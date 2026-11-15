# Qué significan las alertas de Nuclei y Wapiti en una app de tareas

**Autora:** Adriana Rafaela Laos Gonzáles  
**Proyecto desarrollado con:** Antony Piero Solorzano Zegarra

*Artículo de Adriana Rafaela Laos Gonzáles, publicado desde la cuenta de Antony Piero Solorzano Zegarra, integrante del mismo equipo.*

Un escáner puede terminar con varias advertencias sin que todas representen fallos distintos o tengan el mismo impacto. En esta actividad se analizó Campus Tareas, una aplicación con JavaScript y Firestore publicada en GitHub Pages. Se utilizaron Nuclei y Wapiti para revisar la configuración observable desde su URL pública.

Ambas herramientas figuran en la [lista de OWASP](https://community.owasp.org/Vulnerability_Scanning_Tools). Se excluyeron SonarCloud, Snyk y Semgrep, presentes en los workflows académicos revisados.

## Preparar una ejecución reproducible

La aplicación tiene un [repositorio público](https://github.com/AntonyS3010/campus-tareas-nosql) y se despliega con GitHub Actions. El nuevo análisis se ejecuta después de un despliegue correcto. Las versiones de las herramientas quedaron fijadas: Nuclei 3.11.1 y Wapiti 3.3.2.

El script de Nuclei emplea la plantilla oficial firmada `http-missing-security-headers`. Wapiti se limita a `csp`, `http_headers` y `cookieflags`. No se activaron módulos de inyección o fuerza bruta y no se entregaron credenciales del navegador.

Antes de ejecutar los escáneres, el script comprueba la respuesta HTTP y compara el hash del HTML publicado con el del archivo del repositorio. Así se evita confundir un error de conexión o una versión diferente de la web con un resultado válido.

## Nueve coincidencias y tres hallazgos

Nuclei encontró **9 coincidencias informativas**, todas relacionadas con cabeceras de seguridad ausentes. Wapiti clasificó **3 hallazgos como bajos**: CSP, protección contra clickjacking y protección frente a confusión de tipos MIME.

Los resultados coinciden en parte. Se refieren a una misma respuesta HTTP y varias advertencias señalan la misma configuración. Por eso, no se sumaron como doce vulnerabilidades independientes.

La severidad también pertenece al contexto de cada herramienta. Que Nuclei marque una coincidencia como informativa y Wapiti la incluya entre sus hallazgos bajos no es una contradicción: emplean categorías y criterios diferentes.

## Revisar el impacto de cada advertencia

Una CSP define restricciones para los recursos que puede cargar una página. La ausencia de esa política reduce una capa de defensa, pero no demuestra que exista una inyección de JavaScript. En esta app, el contenido de las tareas se inserta con `textContent`; el escaneo realizado no identificó una explotación de XSS.

La advertencia de clickjacking señala que no se encontró `X-Frame-Options`. Se debería evaluar una política de inclusión en marcos mediante esa cabecera o mediante `frame-ancestors` en una cabecera CSP. No basta con añadir cualquier directiva en una etiqueta HTML: algunas protecciones requieren una cabecera de respuesta.

`X-Content-Type-Options: nosniff` indica al navegador que respete el tipo de contenido declarado. La ausencia de esa cabecera debe revisarse junto con los tipos MIME reales que entrega el servidor. El análisis sí observó un tipo de contenido HTML con charset y HSTS en la respuesta.

## El alojamiento también forma parte del resultado

El archivo `firebase.json` contiene una configuración de cabeceras, pero la web se aloja en GitHub Pages. Esa configuración no se aplica a este proveedor. La revisión de la respuesta confirmó la diferencia entre lo declarado en un archivo y lo que recibe el navegador.

Para corregir las cabeceras se necesita un alojamiento o proxy que permita controlarlas. También hay que probar que una CSP no impida las conexiones con Firebase o la carga de sus módulos. En esta actividad se documentaron las medidas posibles, sin afirmar que los hallazgos ya estén corregidos.

## Conservar la evidencia

El workflow guarda los reportes originales de las dos herramientas, sus registros y un resumen. Los archivos permiten revisar el objetivo, las versiones, el commit y la fecha de ejecución. Si las herramientas fallan, el trabajo debe señalarlo; no debe convertir una ausencia de resultados por problemas de red en una conclusión de seguridad.

El alcance de esta prueba fue una URL, sin autenticación y con comprobaciones limitadas de configuración. No se ejecutó todo el flujo JavaScript ni se evaluaron los permisos de Firestore. Esas verificaciones requieren pruebas adicionales.

## Video de la actividad

[Ver la demostración en YouTube (3 min 20 s)](https://www.youtube.com/watch?v=Y0DHOWkfnhU). El recorrido muestra la preparación de las herramientas, el análisis y la lectura de los reportes.

## Enlaces de la actividad

- [Aplicación publicada](https://antonys3010.github.io/campus-tareas-nosql/)
- [Repositorio y reportes](https://github.com/AntonyS3010/campus-tareas-nosql/tree/main/security)
- [Workflow de despliegue](https://github.com/AntonyS3010/campus-tareas-nosql/blob/main/.github/workflows/deploy.yml)
- [Workflow de escaneo](https://github.com/AntonyS3010/campus-tareas-nosql/blob/main/.github/workflows/security.yml)
- [Ejecución verificada del escaneo](https://github.com/AntonyS3010/campus-tareas-nosql/actions/runs/43743571100)

Documentación: [Nuclei](https://github.com/projectdiscovery/nuclei), [plantilla utilizada](https://github.com/projectdiscovery/nuclei-templates/blob/main/http/misconfiguration/http-missing-security-headers.yaml) y [Wapiti](https://wapiti-scanner.github.io/).
