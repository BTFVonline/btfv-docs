# BTFV Verbandsdokumente

Offizielle Dokumente des Bayerischen Tischfußballverbands e.V. (BTFV) als Markdown-Quellen.
Die Website und PDFs werden automatisch per GitHub Actions generiert und auf GitHub Pages veröffentlicht.

---

## Dokumente bearbeiten

Alle Dokumente liegen im Ordner `docs/` als Markdown-Dateien. Nach jedem Push auf `main` werden automatisch:
- die **PDFs** neu generiert und in `assets/pdf/` gespeichert
- die **Website** neu gebaut und auf GitHub Pages deployt

### Datei-Aufbau

Jedes Dokument beginnt mit einem YAML-Header:

```yaml
---
title: "Satzung"
subtitle: "des BTFV e.V."          # optional
date: "{{ site.time | date: '%d.%m.%Y' }}"
section_numbering: paragraph        # paragraph | arabic | weglassen = keine
pdf: /assets/pdf/satzung.pdf       # für Download-Link auf der Website
---
```

### Abschnittsnummerierung

| Wert | Darstellung |
|---|---|
| `paragraph` | § 1, § 1.1, § 1.1.1 … |
| `arabic` | 1, 1.1, 1.1.1 … |
| *(nicht gesetzt)* | Keine automatische Nummerierung |

### Inhaltsverzeichnis

```markdown
* TOC
{:toc}
```

Wird im PDF zu einem automatischen Inhaltsverzeichnis. Auf der Website rendert Jekyll es als verlinkte Liste.

### Datum

```yaml
date: "{{ site.time | date: '%d.%m.%Y' }}"
```

Wird beim PDF-Export automatisch durch das Datum des letzten Commits ersetzt.

### HTML-only-Blöcke

```html
<div class="html-only">
  Dieser Inhalt erscheint nur auf der Website, nicht im PDF.
</div>
```

### Alphabetische Listen

```html
<ol type="a">
  <li>Erster Punkt</li>
  <li>Zweiter Punkt</li>
</ol>
```

Wird im PDF automatisch in eine alphabetisch nummerierte Liste umgewandelt.

---

## Website-Features

Die generierte Website bietet folgende eingebaute Funktionen:

- **PWA** – kann auf iOS und Android als App installiert werden
- **Hell / Dunkel / Auto** – Theme-Toggle im Einstellungs-Menü (Zahnrad)
- **Schriftgröße** – 5-stufiger Regler (70 %–150 %) im Einstellungs-Menü
- **Suche** – In-Page-Suche mit Treffer-Markierung und Navigation
- **Lesefortschritt** – Fortschrittsbalken oben auf der Seite
- **Heading-Links** – Klick auf Überschrift kopiert direkten Link

---

## Neues Dokument anlegen

1. Neue `.md`-Datei in `docs/` erstellen
2. YAML-Header einfügen (siehe oben)
3. Inhalt schreiben
4. **`index.md` aktualisieren** – damit das Dokument auf der Startseite verlinkt wird:
   ```markdown
   | [Mein Dokument](docs/mein-dokument.html) | [PDF](assets/pdf/mein-dokument.pdf) |
   ```
5. `pdf:` ins Front Matter eintragen sobald das PDF nach dem ersten Build vorhanden ist
6. Push auf `main` → PDF und Website werden automatisch aktualisiert

---

## Ausfüllbares Ausschreibungs-Formular

Das Formular `assets/pdf/btfv-challenger-ausschreibung.pdf` entsteht **nicht** aus einer Markdown-Datei,
sondern aus dem HTML-Layout in `forms/`. Es enthält echte PDF-Formularfelder zum Ausfüllen am Rechner.

```bash
bash forms/build.sh   # aus dem Repo-Root, benötigt Microsoft Edge und "pip install pymupdf"
```

Ablauf: `forms/btfv-challenger-ausschreibung.template.html` wird per Headless-Edge nach PDF gerendert,
anschließend setzt `forms/make_fillable.py` die Formularfelder an die Positionen der Linien und Kästchen.
Feldnamen und Reihenfolge stehen oben in `make_fillable.py`; passt die Anzahl nicht mehr zum Layout,
bricht der Build mit einer Meldung ab.

Anforderungen, Feldliste und die Begründungen zu den einzelnen Feldern stehen in
[`forms/README.md`](forms/README.md).

**Wichtig:** Es darf keine `docs/btfv-challenger-ausschreibung.md` geben – der Workflow würde daraus
ein Pandoc-PDF gleichen Namens erzeugen und das Formular überschreiben.

## Technischer Hintergrund

Dieses Repo nutzt das Framework [md-to-web-and-pdf](https://github.com/deluxeGitHub/md-to-web-and-pdf) als reusable Workflow. Layout, Templates und CSS werden automatisch aus dem Framework bezogen – dieses Repo enthält nur die Dokumente selbst.

---

## Lizenz

[UNLICENSE](LICENSE) – Public Domain
