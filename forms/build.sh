#!/usr/bin/env bash
# Rendert das ausfüllbare Ausschreibungs-Formular nach assets/pdf/.
# Aufruf aus dem Repo-Root:  bash forms/build.sh
# Voraussetzungen: Microsoft Edge, Python mit PyMuPDF (pip install pymupdf)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT/forms/btfv-challenger-ausschreibung.template.html"
OUT_HTML="$ROOT/forms/.build/btfv-challenger-ausschreibung.html"
OUT_PDF="$ROOT/assets/pdf/btfv-challenger-ausschreibung.pdf"

mkdir -p "$(dirname "$OUT_HTML")" "$(dirname "$OUT_PDF")"

winpath() { cygpath -w "$1" 2>/dev/null || echo "$1"; }
urlpath()  { cygpath -m "$1" 2>/dev/null || echo "$1"; }

python "$ROOT/forms/make_fillable.py" html "$TEMPLATE" "$OUT_HTML"

EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"$EDGE" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$(winpath "$OUT_PDF")" "file:///$(urlpath "$OUT_HTML")"

python "$ROOT/forms/make_fillable.py" fields "$OUT_PDF"

echo "PDF: $OUT_PDF"
