# Resultados del escaneo

Objetivo: https://antonys3010.github.io/campus-tareas-nosql/
Commit: `813dc71a77c7275e30693b78c464bdc4cccd3995`

## Nuclei

| Comprobación | Severidad de la plantilla |
| --- | --- |
| cross-origin-resource-policy | info |
| content-security-policy | info |
| permissions-policy | info |
| x-frame-options | info |
| x-content-type-options | info |
| x-permitted-cross-domain-policies | info |
| referrer-policy | info |
| cross-origin-embedder-policy | info |
| cross-origin-opener-policy | info |

## Wapiti

| Categoría | Nivel del escáner |
| --- | --- |
| Content Security Policy Configuration | 1 |
| Clickjacking Protection | 1 |
| MIME Type Confusion | 1 |

Wapiti: 0 informativo, 1 bajo, 2 medio, 3 alto y 4 crítico.

Los resultados de ambos escáneres se superponen; no se suman como fallos independientes.
Un trabajo de CI correcto significa que el análisis se ejecutó, no que la aplicación esté libre de vulnerabilidades.
Este alcance no prueba las reglas de Firestore, las operaciones autenticadas ni toda la lógica JavaScript.
Las cabeceras HTTP dependen también del proveedor de alojamiento.
