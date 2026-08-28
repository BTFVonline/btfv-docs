# Ausschreibungs-Formular BTFV-Challenger

Arbeitsdatei für die Weiterentwicklung des Formulars. Sie hält fest, **was das Formular
können muss, wie es gebaut wird und welche Entscheidungen bereits gefallen sind** – damit
das Formular in einem neuen Chat ohne Vorwissen weiterbearbeitet werden kann.

Ergebnis: `assets/pdf/btfv-challenger-ausschreibung.pdf` – ein ausfüllbares PDF auf **einer
A4-Seite**, verlinkt aus `docs/btfv-challengerordnung.md` (Abschnitt „Vorlage für die
Ausschreibung“) und aus `index.md`.

---

## Dateien

| Datei | Zweck |
|---|---|
| `forms/btfv-challenger-ausschreibung.template.html` | Layout des Formulars (HTML + CSS), einzige Quelle für Optik und Zeilen |
| `forms/make_fillable.py` | entfernt Platzhalter, bettet Logos ein, setzt nach dem Rendern die PDF-Formularfelder |
| `forms/build.sh` | Ablaufsteuerung: HTML aufbereiten → Edge rendert PDF → Felder einsetzen |
| `forms/.build/` | Zwischenstände, nicht im Git |

## Bauen

```bash
bash forms/build.sh          # aus dem Repo-Root
```

Voraussetzungen: Microsoft Edge (Headless-Druck) und `pip install pymupdf`.

Ablauf im Detail:

1. `make_fillable.py html` entfernt alle Platzhalter der Form `&lt;…&gt;` aus dem Template
   (die Felder bleiben leer) und bettet die Logos als Base64 ein.
2. Edge druckt das HTML nach `forms/.build/btfv-challenger-ausschreibung.pdf`; erst nach
   dem Einsetzen der Felder wird die Datei nach `assets/pdf/` kopiert. Grund: Ist das PDF
   in `assets/pdf/` gerade in einem Viewer geöffnet, schreibt Edge es nicht neu – Schritt 3
   hätte die Felder sonst ein zweites Mal in die alte Datei gesetzt.
3. `make_fillable.py fields` liest die Vektorzeichnung der Seite, erkennt daran die
   Feldpositionen und setzt echte AcroForm-Felder ein:
   - **Textfeld**: jede waagerechte Linie breiter als 200 pt (die Unterstriche der Zeilen)
   - **Bandfeld**: jede Linie zwischen 25 und 60 pt Breite (die drei kurzen Felder im blauen Band)
   - **Ankreuzfeld**: jedes gefüllte Quadrat zwischen 12 und 18 pt Kantenlänge

Die Zuordnung Feld → Name erfolgt über die Reihenfolge von oben nach unten. Die Listen
`TEXT_FIELDS`, `BAND_FIELDS` und `CHECKBOXES` stehen oben in `make_fillable.py`. **Stimmt die
Anzahl der gefundenen Elemente nicht mit den Listen überein, bricht der Build ab** – dann
wurde das Template geändert, ohne die Listen nachzuziehen.

---

## Harte Rahmenbedingungen

- **Genau eine A4-Seite.** Der Seitencontainer hat feste Höhe und `overflow: hidden`; was
  nicht passt, wird ohne Fehlermeldung abgeschnitten. Nach jeder Änderung das PDF ansehen
  und prüfen, ob das Fußband samt Schlusszeile vollständig sichtbar ist. Stellschraube für
  die Höhe ist in erster Linie `margin-bottom` bei `.row` (aktuell 2,9 mm).
- **Den Restplatz nimmt der Info-Block auf** (`.block.grow`, Grid-Zeile `1fr`), dessen letzte
  Zeile „Sonstiges“ sich dehnt. Eine eigene Füllzeile gibt es nicht mehr: Ein schmaler weißer
  Füllstreifen wurde ab einer Höhe unter 3 pt als Feldlinie erkannt und ließ den Build
  fehlschlagen.
- **Es darf keine `docs/btfv-challenger-ausschreibung.md` geben.** Der Build-Workflow
  erzeugt für jede `docs/*.md` ein Pandoc-PDF gleichen Namens und würde das Formular
  überschreiben. Deshalb liegt die Quelle in `forms/` und `forms/` ist in `_config.yml`
  von Jekyll ausgeschlossen.
- Das fertige PDF ist im Git eingecheckt. Der Workflow macht nur `git add assets/pdf/`,
  löscht dort also nichts.
- Inhalte müssen zur `docs/btfv-challengerordnung.md` passen. Ändert sich die Ordnung,
  muss das Fußband („BTFV-Challenger Standard“) mitgezogen werden.

---

## Aufbau der Seite

Vorbild ist die DTFB-Challenger-Ausschreibung
(<https://dtfb.de/images/dokumente/Turniere/2024_01_Challenger_Ausschreibung_Vorlage.pdf>),
umgesetzt in BTFV-Farben.

```
┌────────┬──────────────────────────────────────────┐
│ FORMAT │ CHALLENGER + BTFV-Logo                   │
│ TURNIER│ Turniername … Turnierstart               │
│        │ ▬ Band: DISZIPLIN & KATEGORIE ▬          │
│        │ Disziplin (Ankreuzfelder), Weitere       │
│        │ ▬ Band: Tische / Startplätze ▬           │
│ TISCHE │ Tischmodelle                             │
│ INFO   │ Anmeldung, Preise, Catering, Sonstiges    │
│ PARTNER│ Leonhart-Badge + Partnerzeile            │
├────────┴──────────────────────────────────────────┤
│ ▬ Band: BTFV-CHALLENGER STANDARD ▬                │
│ Regelauszug in zwei Spalten                       │
└───────────────────────────────────────────────────┘
```

Farben (aus dem BTFV-Logo abgeleitet):

| Rolle | Wert |
|---|---|
| Blau (Bänder, Überschriften) | `#03326c` |
| Helleres Blau (Akzente, Schienenlabel) | `#1663b0` |
| Hellblau (Linien, Kästchen) | `#dfeaf8` |
| Dunkle Schiene und Fußbereich | `#0b1826` |
| Platzhalter- und Eingabetext | Grau `rgb(0.36, 0.42, 0.49)` |

Häkchen der Ankreuzfelder werden als Vektorzeichnung in BTFV-Blau in den
Appearance-Stream geschrieben, damit sie in jedem Reader gleich aussehen. Zusätzlich ist
`/MK /CA (4)` gesetzt, falls ein Reader das Aussehen selbst neu erzeugt.

---

## Felder (Stand: 18.08.2026)

**Textfelder**, in dieser Reihenfolge:

| Feldname | Beschriftung | Hinweis |
|---|---|---|
| `turniername` | Turniername | vorbelegt mit „BTFV-Challenger “ |
| `ausrichter` | Ausrichter / Verein | |
| `ansprechpartner` | Ansprechpartner | Name, E-Mail, Telefon |
| `location` | Location | Spielstätte, Straße, PLZ Ort |
| `datum` | Datum | |
| `einlass` | Einlass | |
| `turnierstart` | Turnierstart | |
| `weitere_disziplin` | Weitere Disziplin | Freitext für Damen, Junioren, Senioren, Mixed |
| `tischmodelle` | Tischmodelle | Anzahl und Modell, nur Tische der BTFV-Tischpartner |
| `anmeldung` | Anmeldung | E-Mail-Adresse oder Link, über den sich Teams melden |
| `preise` | Preise | |
| `catering` | Catering | |
| `sonstiges` | Sonstiges | mehrzeilig, füllt den verbleibenden Platz bis zur Partnerzeile |

**Bandfelder** (blaues Band, kurze Zahlenfelder): `anzahl_tische`,
`startplaetze_doppel`, `startplaetze_einzel`.

**Ankreuzfelder**: `offenes_doppel`, `offenes_einzel`.

---

## Entscheidungen und Begründungen

- **Nur „Offenes Doppel“ und „Offenes Einzel“ als Ankreuzfeld**, alles Weitere über das
  Freitextfeld „Weitere Disziplin“. Begründung: In der Praxis sind fast alle Turniere
  offenes Doppel oder offenes Einzel; ein Raster mit Damen, Junioren, Senioren und Mixed
  war zu viel Fläche für seltene Fälle.
- **Kein Feld für Vorrunde und Playoffs.** Die zulässigen Modi sind in der Ordnung
  geregelt und stehen im Fußband; als Ankreuzfeld waren sie doppelt gepflegt.
- **`sonstiges` ist mehrzeilig** und reicht von der Catering-Zeile bis zur Partnerzeile.
  Dafür ist der Eintrag in `TEXT_FIELDS` um `"multiline"` ergänzt; die Feldhöhe ergibt sich
  aus dem Abstand zur darüberliegenden Linie.
- **Divisionen (Profi/Amateur/Neuling) sind kein Formularfeld.** Die Aufteilung ergibt
  sich aus der Teilnehmerzahl und steht im Fußband beziehungsweise in der Ordnung.
- **Kein Feld für Startgeld.** Die Organisationspauschale ist in der Ordnung mit 10 € je
  Teilnehmer und Disziplin (Junioren 0 €) festgelegt und steht deshalb als feste Angabe im
  Fußband statt als ausfüllbares Feld.
- **Kein Feld für Meldeschluss und maximale Teilnehmerzahl.** Die Teilnehmerzahl steht
  bereits als Startplätze im blauen Band.
- **Kein Feld für Figuren und Bälle.** Ergibt sich aus dem Tischmodell; die Anforderung
  steht im Fußband.
- **Feld „Anmeldung“ bleibt**, weil sich Teams oft über eine andere Adresse oder einen
  Turnierlink melden als beim Ansprechpartner. Wenn beides zusammenfällt, kann das Feld
  ersatzlos entfallen.
- **Partnerzeile**: „Partner der BTFV-Tour: Original Leonhart – Kickertische &
  Tischfußball, Made in Germany.“ Schreibweise und Claim von
  <https://original-leonhart.com> übernommen; die Marke heißt „Original Leonhart“,
  nicht „Leonhart Tischfußball“.

## Wenn etwas geändert werden soll

1. Zeile im Template ergänzen oder entfernen (`.row` mit `.k` als Beschriftung und `.v`
   als Linie, oder `.opts` mit `.cb`-Kästchen für Ankreuzfelder).
2. Passenden Eintrag in `TEXT_FIELDS`, `BAND_FIELDS` oder `CHECKBOXES` an derselben
   Position ergänzen oder entfernen – die Reihenfolge entspricht der Position auf der Seite.
3. `bash forms/build.sh` ausführen und das PDF ansehen: passt alles auf eine Seite, ist
   die Schlusszeile im Fußband vollständig, sitzen die Felder auf den Linien?
4. Zum Testen die Felder probeweise füllen (PyMuPDF: `widget.field_value = …` und
   `widget.update()`), damit die Position des Eingabetexts geprüft werden kann.
