
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
