# X40 Sensor-Hub für Raspberry Pi 5

[cite_start]Ein modulares Framework zur dynamischen Auslesung und Visualisierung von Sensordaten aus dem **Joy-IT X40-Sensorkit**[cite: 1]. [cite_start]Dieses Projekt wurde als Schulprojekt entwickelt und ist gezielt für die Nutzung mit einem **Touchscreen** am Raspberry Pi 5 optimiert[cite: 5, 6].

## ✨ Features
* [cite_start]**Dynamisches Dashboard:** Sensoren können zur Laufzeit über die GUI ausgewählt und konfiguriert werden[cite: 25, 56].
* [cite_start]**Touch-Optimiert:** Große interaktive Flächen und intuitive Menüführung ohne verschachtelte Untermenüs[cite: 6, 29].
* [cite_start]**Integrierter Anschluss-Guide:** Die Software zeigt direkt an, welcher Sensor an welchen Pin (GPIO oder ADC) angeschlossen werden muss[cite: 7, 34].
* [cite_start]**Echtzeit-Performance:** Dank Multithreading (Hintergrund-Thread für Sensoren) bleibt die GUI jederzeit reaktionsfähig[cite: 9, 53].
* [cite_start]**Hardware-Abstraktion:** Einfache Integration von digitalen und analogen Sensoren via ADS1115 ADC[cite: 4, 33].

| Live-Monitor | Anschluss-Guide |
| :---: | :---: |
| <img src="docs/Oberview.jpg" width="400"> | <img src="docs/AnschlussPlan.jpg" width="400"> |

## 🛠 Technische Details
* [cite_start]**Sprache:** Python[cite: 10].
* [cite_start]**Architektur:** Modulare Ebenen (Präsentation, Logik, Hardware) für leichte Erweiterbarkeit[cite: 11, 64].
* [cite_start]**Hardware:** Raspberry Pi 5, ADS1115 (KY-053) Analog-Digital-Wandler[cite: 30, 33].
* [cite_start]**Besonderheit:** Anpassung an die neue **RP1-I/O-Architektur** des Pi 5 durch Nutzung moderner CircuitPython-Bibliotheken[cite: 45, 50].

## 🚀 Installation & Start
1. Repository klonen.
2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
