
## Aktueller Stand - Woche 7

Die praktische Implementierung des Projekts wurde begonnen.

### Bereits umgesetzt

- Python-Projekt mit Git-Versionskontrolle
- X-COBOL-Datensatz heruntergeladen und untersucht
- Einfacher COBOL-Dateileser
- Prototyp zur Erkennung von GO TO und ALTER
- Grundlegende Verarbeitung von Kommentaren und Literalen
- Automatisierte Tests mit pytest

### Validierung

Der Analysator wird zunächst mit kleinen,
kontrollierten COBOL-Beispielen getestet.

Die Tests überprüfen unter anderem:
- Erkennung von GO TO und ALTER
- Kommentare und Zeichenketten
- Groß- und Kleinschreibung
- Fehlerbehandlung

### Bekannte Einschränkungen

Der Analysator unterstützt noch nicht alle
COBOL-Dialekte und Quellcodeformate.

Fortsetzungen von Zeilen werden noch nicht
vollständig unterstützt.

Die Ergebnisse sind bisher nur ein Proof of Concept
und keine endgültigen Forschungsergebnisse.

### Nächste Schritte

- Erste echte X-COBOL-Dateien analysieren
- Erkennungsregeln weiter validieren
- Metadaten mit Analyseergebnissen verbinden
- Experimentellen Teil für Woche 9 vorbereiten
```



## Installation und Ausführung

Voraussetzung: Python 3.12

### 1. Entwicklungsabhängigkeiten installieren

python -m pip install -r requirements-dev.txt

### 2. Analysator starten

python main.py

Der Analysator untersucht zunächst eine kleine
COBOL-Beispieldatei und zählt die erkannten
GO-TO- und ALTER-Vorkommen.

### 3. Automatisierte Tests ausführen

python -m pytest -q

### 4. X-COBOL-Datensatz untersuchen

Der X-COBOL-Datensatz (Ali et al., 2023)
muss separat heruntergeladen und unter
data/X-COBOL/ entpackt werden.

python inspect_dataset.py

## Status in Woche 7

Der aktuelle Stand ist ein ausführbarer
Proof of Concept für die statische Analyse.

Die Erkennung wurde mit kontrollierten
COBOL-Beispielen getestet. Die vollständige
empirische Untersuchung ist noch nicht
abgeschlossen.

Als Nächstes sollen echte X-COBOL-Dateien
untersucht und die Erkennungsregeln weiter
validiert werden.

## Woche 9 – Vorbereitung der Fallstudie

Für die Fallstudie wird ein kleiner, reproduzierbarer
Datenausschnitt aus X-COBOL vorbereitet.

### Datenauswahl

Das Skript `prepare_sample.py` sucht nach Dateien
mit COBOL-Dateiendungen und wählt maximal 15
Dateien mit einem festen Zufalls-Seed aus.

Die Auswahl wird in
`results/selected_files.csv` gespeichert.

Die Auswahl ist vorläufig. Vor der eigentlichen
Analyse müssen die Dateiformate und die
Zuordnung zu den Metadaten überprüft werden.

### Metadaten

Mit `inspect_metadata.py` werden die verfügbaren
CSV-Dateien und ihre Spalten untersucht.

Ziel ist die spätere Zuordnung von Quelldateien
zu Repository, Commit-Anzahl und LOC.

### Ausführung

python prepare_sample.py
python inspect_metadata.py
python -m pytest -q

### Nächste Schritte

- Quelldateien mit Metadaten verknüpfen
- Kompatible COBOL-Dateien identifizieren
- Den Analysator auf dem Datenausschnitt ausführen
- Warnungen und Warnungsdichte berechnen
- Erste Ergebnisse manuell validieren

## Woche 9 – Experimenteller Proof of Concept

### Erste Analyse realer COBOL-Dateien

Das Skript `run_experiment.py` verwendet die zuvor
ausgewählten Dateien aus dem X-COBOL-Datensatz.

Für jede Datei werden folgende Informationen erfasst:

- Dateipfad
- angenommener COBOL-Quelltextformattyp
- Anzahl der erkannten GO-TO-Vorkommen
- Anzahl der erkannten ALTER-Vorkommen
- Gesamtzahl der erkannten Warnungen
- Anzahl der analysierten Codezeilen
- vorläufige Warnungsdichte
- eventuelle Analysefehler

Die Ergebnisse werden in
`results/experiment_results.csv` gespeichert.

### Ausführung

python run_experiment.py
python -m pytest -q

### Einschränkungen

Der Analysator ist noch kein vollständiger COBOL-Parser.

Die erste experimentelle Ausführung nimmt das
Fixed-Format an. Die tatsächlichen Quelltextformate
müssen noch geprüft werden.

Die aktuelle LOC-Metrik basiert auf nichtleeren
Zeilen nach der Vorverarbeitung und ist nicht
identisch mit einer offiziellen CLOC-Messung.

Erfolgreiche Ausführung bedeutet nicht automatisch,
dass alle erkannten Warnungen korrekt sind.

Die Zuordnung von Commits und offiziellen LOC-Werten
aus X-COBOL sowie die manuelle Validierung sind
noch ausstehend.

### Nächste Schritte

- Quelltextformate überprüfen
- Dateimetadaten zuordnen
- Ergebnisse manuell validieren
- Ergebnisse interpretieren
- Die vorläufige Fallstudie im L4-Bericht darstellen


### Manual Validation Results

For the initial validation, three COBOL files from
different repositories were manually inspected:

- CSF00600.cpy
- TCPYB01.cpy
- clinkages.cbl

The manual review included:
- Checking the COBOL source format (fixed or free)
- Searching for GO TO and ALTER instructions
- Checking whether occurrences appear in executable
  code, comments, or string literals
- Comparing the findings with the analyzer results

The review results are documented in:
results/zero_review.csv

This validation helps identify possible missed
warnings and limitations of the current analyzer.


### Preliminary Experimental Results

The initial experiment selected 15 COBOL files
from the X-COBOL dataset.

Results:
- Successfully processed files: 15
- Failed files: 0
- Manually verified source formats in experiment: 2
- Detected GO TO occurrences: 0
- Detected ALTER occurrences: 0
- Automated tests passed: 26

Three files were additionally inspected manually
for possible missed GO TO and ALTER instructions.

No such instructions were found in these three files.

These results are preliminary because the remaining
source formats have not all been manually verified.

The absence of detected warnings in this sample
does not establish that the full X-COBOL dataset
contains no such constructs.

File-level commit metadata and verified LOC values
still need to be integrated before statistical analysis.
