"""Escaneo acotado de la página pública de Campus Tareas."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = "https://antonys3010.github.io/campus-tareas-nosql/"
parser = argparse.ArgumentParser()
parser.add_argument("--output", default="security/reports/latest")
args = parser.parse_args()
output = Path(args.output).resolve()
output.mkdir(parents=True, exist_ok=True)
for executable in ("nuclei", "wapiti"):
    if not shutil.which(executable):
        raise SystemExit(f"Falta instalar {executable}.")

with urllib.request.urlopen(TARGET, timeout=30) as response:
    html = response.read()
    if response.status != 200 or response.geturl() != TARGET:
        raise SystemExit("La página publicada no respondió en la URL esperada.")
    headers = dict(response.headers)
expected_hash = hashlib.sha256((ROOT / "public/index.html").read_bytes()).hexdigest()
received_hash = hashlib.sha256(html).hexdigest()
if received_hash != expected_hash:
    raise SystemExit("La página publicada no coincide con public/index.html del checkout.")
(output / "response-headers.json").write_text(json.dumps(headers, indent=2))
commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
metadata = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "target": TARGET,
            "source_commit": commit, "html_sha256": received_hash,
            "nuclei": "3.11.1", "wapiti": "3.3.2",
            "nuclei_template_blob": "7c1c5b8191ddf3468348b8f8a046b4d61b75d319",
            "scope": "Una URL pública; cabeceras HTTP, CSP y atributos de cookies. Sin sesión de Firebase."}

def run(command, name, timeout=180):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    log = result.stdout + result.stderr
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        log = log.replace(proxy, "[proxy del entorno]")
    (output / f"{name}.log").write_text(log)
    if result.returncode:
        raise RuntimeError(f"{name} terminó con error {result.returncode}. Revisar su registro.")
    return log

nuclei = ["nuclei", "-u", TARGET, "-t", "security/templates/http-missing-security-headers.yaml",
          "-rl", "1", "-c", "1", "-bs", "1", "-timeout", "10", "-retries", "1",
          "-duc", "-ni", "-no-stdin", "-nc", "-omit-raw", "-jsonl", "-o", str(output / "nuclei.jsonl")]
proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if proxy:
    nuclei += ["-proxy", proxy, "-proxy-internal"]
nuclei_log = run(nuclei, "nuclei")
if "Could not execute request" in nuclei_log or "no address found" in nuclei_log:
    raise RuntimeError("Nuclei no pudo realizar la solicitud; no es un resultado limpio.")
if "Templates loaded for current scan: 1" not in nuclei_log:
    raise RuntimeError("No se confirmó la carga de la plantilla de Nuclei.")

run(["wapiti", "-u", TARGET, "--scope", "url", "--headless", "no", "-m", "csp,http_headers,cookieflags",
     "--tasks", "1", "-d", "0", "--max-scan-time", "90", "--max-attack-time", "30", "-t", "10",
     "--verify-ssl", "1", "--no-bugreport", "--store-session", str(output / "session"),
     "-f", "json", "-o", str(output / "wapiti.json")], "wapiti")
findings = [json.loads(row) for row in (output / "nuclei.jsonl").read_text().splitlines() if row.strip()]
wapiti = json.loads((output / "wapiti.json").read_text())
categories = {key: rows for key, rows in wapiti.get("vulnerabilities", {}).items() if rows}
metadata["nuclei_matches"] = len(findings)
metadata["wapiti_findings"] = sum(map(len, categories.values()))
(output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
lines = ["# Resultados del escaneo", "", f"Objetivo: {TARGET}", f"Commit: `{commit}`", "",
         "## Nuclei", "", "| Comprobación | Severidad de la plantilla |", "| --- | --- |"]
lines += [f"| {item.get('matcher-name', item['template-id'])} | {item['info']['severity']} |" for item in findings]
lines += ["", "## Wapiti", "", "| Categoría | Nivel del escáner |", "| --- | --- |"]
for category, rows in categories.items():
    lines += [f"| {category} | {row['level']} |" for row in rows]
lines += ["", "Wapiti: 0 informativo, 1 bajo, 2 medio, 3 alto y 4 crítico.", "",
          "Los resultados de ambos escáneres se superponen; no se suman como fallos independientes.",
          "Un trabajo de CI correcto significa que el análisis se ejecutó, no que la aplicación esté libre de vulnerabilidades.",
          "Este alcance no prueba las reglas de Firestore, las operaciones autenticadas ni toda la lógica JavaScript.",
          "Las cabeceras HTTP dependen también del proveedor de alojamiento."]
(output / "summary.md").write_text("\n".join(lines) + "\n")
print(json.dumps(metadata, ensure_ascii=False, indent=2))
