# csvstat

`csvstat` ist ein schlankes Kommandozeilenwerkzeug, das eine CSV-Datei einliest
und je Spalte eine kurze Statistik ausgibt: für numerische Spalten `count`,
`min`, `max`, `mean` und die Anzahl fehlender Werte (`missing`), für Textspalten
`count` und die Anzahl eindeutiger Werte (`unique`). Ob eine Spalte als
numerisch gilt, entscheidet sich daran, ob alle ihre nicht-leeren Werte als
Zahl lesbar sind; gemischte Spalten werden als Text berichtet.

## Tech Stack

- Python 3.11 oder neuer
- Ausschließlich die Python-Standardbibliothek zur Laufzeit:
  `argparse`, `csv`, `json`, `statistics` — keine externen Laufzeitabhängigkeiten.
- `pyproject.toml` mit dem Konsolen-Skript `csvstat`
- `pytest` als reine Entwicklungs-/Test-Abhängigkeit

## Installation

```sh
pip install -e .
```

Für die Tests zusätzlich die Entwicklungs-Extras installieren:

```sh
pip install -e ".[dev]"
```

## Verwendung

Nach der Installation steht das Kommando `csvstat` zur Verfügung; alternativ
startet `python -m csvstat` dasselbe Programm.

```sh
csvstat data.csv
python -m csvstat data.csv
```

Optionen:

- `--delimiter <zeichen>` — Trennzeichen der CSV-Datei (Standard: `,`).
  Beispiel: `csvstat --delimiter ';' data.csv`
- `--columns <name>,<name>,...` — nur diese Spalten berichten, in genau der
  angegebenen Reihenfolge. Beispiel: `csvstat --columns betrag,ort data.csv`
- `--json` — den Bericht als ein gültiges JSON-Dokument ausgeben statt als
  ausgerichteten Text. Beispiel: `csvstat --json data.csv`

Der vollständige Aufruf zur Übersicht aller Optionen:

```sh
python -m csvstat --help
```

Fehler (fehlende Datei, leere Datei, unbekannte Spalte) werden als eine einzelne
Zeile auf stderr gemeldet; der Prozess endet dann mit Exit-Code 1 und ohne
Traceback.

## Tests

```sh
pytest
```
