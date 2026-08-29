#!/usr/bin/env python3
"""Baut aus dem HTML-Template das ausfüllbare Ausschreibungs-PDF.

Ablauf:
1. Platzhalter (<...>) aus dem Template entfernen und Logos einbetten
2. HTML per Headless-Edge nach PDF rendern (macht der Aufrufer, forms/build.sh)
3. Aus der Zeichnung des PDFs die Feldpositionen ableiten (Unterstriche und
   Ankreuzkästchen) und an diesen Stellen echte AcroForm-Felder einsetzen
"""
import base64
import io
import os
import re
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAY = (0.36, 0.42, 0.49)

# Textfelder in Layout-Reihenfolge (oben nach unten): Name, Tooltip, Vorbelegung,
# optional "multiline" – dann reicht das Feld bis zur Zeile darueber
TEXT_FIELDS = [
    ("turniername",       "Turniername",                            "BTFV-Challenger "),
    ("ausrichter",        "Ausrichter / Verein",                    ""),
    ("ansprechpartner",   "Ansprechpartner: Name, E-Mail, Telefon", ""),
    ("location",          "Spielstätte, Straße Hausnummer, PLZ Ort", ""),
    ("datum",             "Datum (TT.MM.JJJJ)",                     ""),
    ("einlass",           "Einlass (hh:mm)",                        ""),
    ("turnierstart",      "Turnierstart (hh:mm)",                   ""),
    ("weitere_disziplin", "Weitere Disziplin, z. B. Damen, Junioren, Senioren, Mixed", ""),
    ("tischmodelle",      "Tischmodelle mit Anzahl – nur Tische der BTFV-Tischpartner", ""),
    ("anmeldung",         "Anmeldung: E-Mail-Adresse oder Link",    ""),
    ("preise",            "Preise",                                 ""),
    ("catering",          "Catering",                               ""),
    ("sonstiges",         "Sonstiges",                              "", "multiline"),
]

# Kurze Felder im blauen Band (links nach rechts)
BAND_FIELDS = [
    ("anzahl_tische",       "Anzahl der Tische"),
    ("startplaetze_doppel", "Startplätze Doppel"),
    ("startplaetze_einzel", "Startplätze Einzel"),
]

# Ankreuzfelder in Layout-Reihenfolge (zeilenweise, links nach rechts)
CHECKBOXES = [
    "offenes_doppel", "offenes_einzel",
]


def build_html(template, out_html):
    html = io.open(template, encoding="utf-8").read()
    html = re.sub(r"&lt;[^&]*&gt;", "", html)  # Platzhalter entfernen, Felder bleiben leer

    def b64(name):
        with open(os.path.join(ROOT, "docs", "images", name), "rb") as fh:
            return base64.b64encode(fh.read()).decode()

    html = html.replace("__LOGO__", b64("btfv-logo.png"))
    html = html.replace("__LEONHART__", b64("powered_by_leonhart.png"))
    io.open(out_html, "w", encoding="utf-8").write(html)


def collect_geometry(page):
    """Unterstriche und Kästchen aus den Vektorzeichnungen des PDFs holen."""
    rules, band_rules, boxes = [], [], []
    for drawing in page.get_drawings():
        r = drawing["rect"]
        if r.height < 3 and r.width > 200:
            rules.append(r)
        elif r.height < 3 and 25 < r.width < 60:
            band_rules.append(r)
        elif 12 < r.width < 18 and 12 < r.height < 18 and drawing.get("fill"):
            boxes.append(r)

    def dedupe(rects, tol=2.0):
        out = []
        for r in sorted(rects, key=lambda x: (round(x.y0, 0), x.x0)):
            if not any(abs(r.y0 - o.y0) < tol and abs(r.x0 - o.x0) < tol for o in out):
                out.append(r)
        return out

    return dedupe(rules), dedupe(band_rules), dedupe(boxes)


def _restyle_checkmarks(doc, page):
    """Häkchen als Vektorzeichnung statt Dingbats-Zeichen setzen.

    Damit sieht das Kreuz in jedem Reader gleich aus und hängt nicht davon ab,
    ob die Schrift ZapfDingbats verfügbar ist.
    """
    for widget in page.widgets():
        if widget.field_type != fitz.PDF_WIDGET_TYPE_CHECKBOX:
            continue
        kind, ref = doc.xref_get_key(widget.xref, "AP/N/Yes")
        if kind != "xref":
            continue
        xref = int(ref.split()[0])
        w, h = widget.rect.width, widget.rect.height
        stream = "\n".join([
            "q",
            "0.01 0.20 0.42 RG",
            "%.2f w" % (w * 0.13),
            "1 J 1 j",
            "%.2f %.2f m %.2f %.2f l %.2f %.2f l S" % (
                w * 0.20, h * 0.52,
                w * 0.42, h * 0.26,
                w * 0.80, h * 0.74,
            ),
            "Q",
        ])
        doc.update_stream(xref, stream.encode("latin-1"))
        # Falls ein Reader das Aussehen selbst neu erzeugt: Häkchen (ZapfDingbats „4“)
        doc.xref_set_key(widget.xref, "MK/CA", "(4)")


def add_fields(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    rules, band_rules, boxes = collect_geometry(page)

    for name, count, want in (
        ("Unterstriche", len(rules), len(TEXT_FIELDS)),
        ("Bandfelder", len(band_rules), len(BAND_FIELDS)),
        ("Kästchen", len(boxes), len(CHECKBOXES)),
    ):
        if count != want:
            raise SystemExit(f"Layout passt nicht: {count} {name} gefunden, erwartet {want}")

    for i, (rule, field) in enumerate(zip(rules, TEXT_FIELDS)):
        name, tip, value = field[:3]
        multiline = len(field) > 3 and field[3] == "multiline"
        top = rules[i - 1].y0 + 4 if multiline and i else rule.y0 - 13.5
        w = fitz.Widget()
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.rect = fitz.Rect(rule.x0 + 1, top, rule.x1 - 1, rule.y0 + 1.5)
        w.field_name = name
        w.field_label = tip
        w.field_value = value
        w.text_fontsize = 9.5
        w.text_color = GRAY
        w.border_width = 0
        if multiline:
            w.field_flags |= fitz.PDF_TX_FIELD_IS_MULTILINE
        page.add_widget(w)

    for rule, (name, tip) in zip(band_rules, BAND_FIELDS):
        w = fitz.Widget()
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.rect = fitz.Rect(rule.x0, rule.y0 - 12.5, rule.x1, rule.y0 + 1)
        w.field_name = name
        w.field_label = tip
        w.field_value = ""
        w.text_fontsize = 10
        w.text_color = (1, 1, 1)
        w.text_maxlen = 4
        w.border_width = 0
        page.add_widget(w)

    for box, name in zip(boxes, CHECKBOXES):
        w = fitz.Widget()
        w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        w.rect = box
        w.field_name = name
        w.field_label = name.replace("_", " ")
        w.field_value = False
        w.border_width = 0
        w.text_color = (0.01, 0.20, 0.42)
        page.add_widget(w)

    _restyle_checkmarks(doc, page)

    doc.set_metadata({
        "title": "Ausschreibung BTFV-Challenger",
        "author": "Bayerischer Tischfußballverband e.V.",
        "subject": "Formular zur Ausschreibung eines BTFV-Challengers",
    })
    doc.saveIncr()
    return len(rules) + len(band_rules) + len(boxes)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "html":
        build_html(sys.argv[2], sys.argv[3])
    elif mode == "fields":
        print(f"{add_fields(sys.argv[2])} Formularfelder eingefügt")
    else:
        raise SystemExit("Aufruf: make_fillable.py html|fields ...")
