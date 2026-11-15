# Escaneo de vulnerabilidades de Campus Tareas

Integrantes: Antony Piero Solorzano Zegarra y Adriana Rafaela Laos Gonzáles.

## Herramientas y selección

Se utilizan **Nuclei 3.11.1** y **Wapiti 3.3.2**, ambos incluidos en la lista de herramientas de escaneo de OWASP. Se excluyeron SonarCloud, Snyk y Semgrep porque aparecen en los workflows `sonar.yml` y `snyk-semgrep.yml` del [examen U1 de Antony](https://github.com/UPT-FAING-EPIS/si784-2026-ii-si784-2026-ii-examen-u1-antonys3010/tree/main/.github/workflows). La revisión no demuestra qué se usó en todas las sesiones de clase; documenta las herramientas identificadas en los repositorios accesibles.

## Objetivo y alcance

URL: https://antonys3010.github.io/campus-tareas-nosql/

El análisis se limita a esa URL de la aplicación del equipo. Nuclei ejecuta una plantilla oficial firmada para cabeceras de seguridad, con una petición por segundo y una sola plantilla concurrente. Wapiti utiliza únicamente `csp`, `http_headers` y `cookieflags`, sin navegador headless y con alcance `url`. No se proporcionan credenciales ni cookies del navegador. No se activan módulos de inyección, fuerza bruta o ejecución de comandos.

Antes de escanear, el script comprueba el estado HTTP y que el SHA-256 del HTML publicado coincida con `public/index.html` del checkout. Un error de conexión se trata como fallo de la ejecución, no como ausencia de vulnerabilidades.

## Resultado inicial

El [resumen](reports/baseline/summary.md) y los reportes originales están en `reports/baseline/`.

| Herramienta | Resultado | Interpretación |
| --- | --- | --- |
| Nuclei | 9 coincidencias informativas | Ausencia de determinadas cabeceras HTTP |
| Wapiti | 3 hallazgos de nivel bajo | CSP ausente, protección contra clickjacking ausente y `X-Content-Type-Options` ausente |

Los resultados coinciden en parte: **no representan 12 vulnerabilidades independientes**. La falta de una cabecera no demuestra una explotación de XSS, acceso a documentos ajenos ni ejecución remota. HSTS y el tipo de contenido con charset sí se observaron en la respuesta.

## Interpretación y medidas

- **CSP:** definir una política compatible con el SDK de Firebase y probar las operaciones de la app antes de aplicarla. Una política en una etiqueta `meta` tiene limitaciones y no equivale a todas las protecciones de una cabecera HTTP.
- **Clickjacking:** establecer `frame-ancestors` en una cabecera CSP o una política `X-Frame-Options` apropiada al uso de la aplicación.
- **MIME:** servir tipos de contenido correctos y `X-Content-Type-Options: nosniff`.
- **Otras cabeceras:** revisar permisos, referencias y aislamiento según las necesidades reales; no activar restricciones que rompan recursos externos sin probarlas.

La aplicación se aloja en GitHub Pages. El archivo `firebase.json` del repositorio no configura las cabeceras de ese proveedor. Por eso, que una cabecera esté declarada allí no demuestra que el sitio publicado la entregue. Para controlar todas las cabeceras se requeriría un alojamiento o proxy que permita configurarlas.

No se cambió de proveedor ni se modificaron las reglas de Firestore como parte de este análisis. Los hallazgos se mantienen documentados; no se declaran corregidos.

## Automatización

`.github/workflows/security.yml` se ejecuta después de un despliegue correcto de `Comprobar y publicar Campus` y también permite ejecución manual. Instala las versiones fijadas de los escáneres, verifica el binario oficial de Nuclei mediante SHA-256 y analiza el sitio publicado. Conserva reportes JSON, registros, metadatos y un resumen como artefactos de GitHub Actions durante 30 días.

Un trabajo correcto confirma que el análisis pudo ejecutarse. Los hallazgos de configuración siguen apareciendo en el reporte y no se ocultan para obtener un estado verde.

## Ejecución local

Con Python 3.12 y los permisos para analizar la aplicación:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r security/requirements.txt
python scripts/install-nuclei.py .tools
PATH="$PWD/.tools:$PATH" python scripts/security-scan.py
```

El script acepta `--output` para seleccionar otro directorio de resultados. El objetivo y los módulos están fijados en el código para mantener este alcance.

## Plantilla utilizada

`templates/http-missing-security-headers.yaml` procede del [repositorio oficial de Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates/blob/main/http/misconfiguration/http-missing-security-headers.yaml), blob `7c1c5b8191ddf3468348b8f8a046b4d61b75d319`. Se conserva su firma y licencia MIT. No se descarga todo el catálogo de plantillas para esta tarea.

## Límites

Este escaneo sin autenticación no ejecuta el flujo JavaScript ni verifica las reglas de Firestore, la autorización por usuario o la lógica de negocio. No es una auditoría completa. Los resultados describen la respuesta y el alcance examinados en la fecha registrada en `metadata.json`.

## Fuentes

- https://community.owasp.org/Vulnerability_Scanning_Tools
- https://github.com/projectdiscovery/nuclei
- https://github.com/projectdiscovery/nuclei-templates
- https://wapiti-scanner.github.io/
- https://github.com/wapiti-scanner/wapiti
