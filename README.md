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

## Technischer Hintergrund

Dieses Repo nutzt das Framework [md-to-web-and-pdf](https://github.com/deluxeGitHub/md-to-web-and-pdf) als reusable Workflow. Layout, Templates und CSS werden automatisch aus dem Framework bezogen – dieses Repo enthält nur die Dokumente selbst.

---

## Lizenz

[UNLICENSE](LICENSE) – Public Domain
