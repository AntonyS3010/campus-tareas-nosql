"""Instala la distribución oficial de Nuclei y comprueba su SHA-256."""
import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

VERSION = "3.11.1"
destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
archive = f"nuclei_{VERSION}_linux_amd64.zip"
checksums = f"nuclei_{VERSION}_checksums.txt"
base = f"https://github.com/projectdiscovery/nuclei/releases/download/v{VERSION}/"
for filename in (archive, checksums):
    urllib.request.urlretrieve(base + filename, destination / filename)
expected = next(line.split()[0] for line in (destination / checksums).read_text().splitlines()
                if line.split()[-1] == archive)
actual = hashlib.sha256((destination / archive).read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit("La suma de verificación de Nuclei no coincide.")
with zipfile.ZipFile(destination / archive) as package:
    (destination / "nuclei").write_bytes(package.read("nuclei"))
(destination / "nuclei").chmod(0o755)
print(f"Nuclei {VERSION}: SHA-256 verificado.")
