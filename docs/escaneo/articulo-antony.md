# Escanear la aplicación publicada: Nuclei y Wapiti en Campus Tareas

**Autor:** Antony Piero Solorzano Zegarra  
**Proyecto desarrollado con:** Adriana Rafaela Laos Gonzáles

Campus Tareas ya estaba publicada en GitHub Pages y guardaba sus datos en Cloud Firestore. Para esta actividad se revisó la respuesta de la aplicación con Nuclei y Wapiti. Ambas figuran en la [lista de escáneres de OWASP](https://community.owasp.org/Vulnerability_Scanning_Tools). Se eligieron herramientas distintas de SonarCloud, Snyk y Semgrep, presentes en los workflows académicos revisados.

## Qué se analizó

La URL examinada fue `https://antonys3010.github.io/campus-tareas-nosql/`. El alcance se limitó a esa página, sus cabeceras HTTP, su política CSP y los atributos de las cookies que pudiera entregar. No se utilizaron credenciales de Firebase.

Nuclei ejecutó una sola plantilla oficial firmada, `http-missing-security-headers`, con una petición por segundo y concurrencia de una plantilla. Wapiti utilizó únicamente los módulos `csp`, `http_headers` y `cookieflags`, con alcance `url` y sin navegador headless.

No se activaron módulos de inyección ni se analizaron las operaciones autenticadas de Firestore. Los resultados no permiten afirmar que toda la aplicación sea segura ni que las reglas de la base de datos sean incorrectas.

## Instalación y ejecución

Se fijaron Nuclei 3.11.1 y Wapiti 3.3.2. El instalador incluido en el repositorio descarga la distribución oficial de Nuclei y comprueba su SHA-256. Para reproducir el análisis desde el repositorio:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r security/requirements.txt
python scripts/install-nuclei.py .tools
PATH="$PWD/.tools:$PATH" python scripts/security-scan.py
```

El script comprueba primero que la URL responda con HTTP 200. También compara el SHA-256 del HTML recibido con `public/index.html`, para vincular el análisis con el código del checkout.

Durante la primera prueba local, Nuclei no pudo resolver el nombre del sitio. Aunque terminó sin coincidencias, ese resultado no se tomó como un escaneo limpio. Se configuró el proxy ya disponible en el entorno y se repitió la ejecución. La nueva prueba confirmó una respuesta HTTP y registró los hallazgos.

## Los resultados

Nuclei reportó **9 coincidencias informativas** por cabeceras ausentes. Wapiti reportó **3 hallazgos bajos**:

| Categoría de Wapiti | Observación |
| --- | --- |
| Content Security Policy Configuration | No se encontró una política CSP |
| Clickjacking Protection | No se encontró X-Frame-Options |
| MIME Type Confusion | No se encontró X-Content-Type-Options |

Los tres puntos también aparecen entre las comprobaciones de Nuclei. No corresponde sumar ambos resultados como doce vulnerabilidades independientes. Una cabecera ausente es un hallazgo de configuración; por sí sola no demuestra una explotación de XSS o la lectura de documentos ajenos.

HSTS y el tipo de contenido HTML con charset sí estaban presentes. Las demás cabeceras se deben evaluar según las necesidades de la app: activar restricciones sin comprobar su efecto puede romper recursos externos.

## Lo declarado en un archivo y la respuesta real

El repositorio conserva un `firebase.json` que declara cabeceras de seguridad. Sin embargo, la web se sirve desde GitHub Pages. Esa configuración de Firebase no modifica la respuesta de GitHub Pages.

Encontrar `nosniff` en un archivo no basta para afirmar que el servidor lo envía. La respuesta publicada es lo que debe comprobarse. Los hallazgos se dejaron documentados y no se presentan como corregidos. Para administrar estas cabeceras habría que utilizar un alojamiento o proxy que permita configurarlas y volver a probar el funcionamiento del SDK de Firebase.

## Automatización después del despliegue

La app se despliega mediante GitHub Actions. Cuando termina correctamente el workflow `Comprobar y publicar Campus`, otro workflow ejecuta Nuclei y Wapiti. También admite ejecución manual.

La [ejecución verificada](https://github.com/AntonyS3010/campus-tareas-nosql/actions/runs/43743571100) terminó correctamente y coincidió con la prueba local. Conserva los reportes JSON, registros, metadatos y resumen como artefactos durante 30 días. La evidencia inicial también está versionada en el repositorio.

Un estado verde indica que las herramientas se ejecutaron correctamente; las advertencias permanecen en los reportes. No certifica que la aplicación esté libre de vulnerabilidades.

## Video de la actividad

[Ver la demostración en YouTube (3 min 20 s)](https://www.youtube.com/watch?v=Y0DHOWkfnhU). Incluye la instalación, el alcance, la automatización y los resultados del análisis.

## Código y evidencias

- [Repositorio público](https://github.com/AntonyS3010/campus-tareas-nosql)
- [Aplicación publicada](https://antonys3010.github.io/campus-tareas-nosql/)
- [Configuración, alcance y reportes](https://github.com/AntonyS3010/campus-tareas-nosql/tree/main/security)
- [Workflow de despliegue](https://github.com/AntonyS3010/campus-tareas-nosql/blob/main/.github/workflows/deploy.yml)
- [Workflow del escaneo](https://github.com/AntonyS3010/campus-tareas-nosql/blob/main/.github/workflows/security.yml)

Fuentes: [Nuclei](https://github.com/projectdiscovery/nuclei), [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates) y [Wapiti](https://wapiti-scanner.github.io/).