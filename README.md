# X40-Sensor-Hub-for-Raspberry-Pi-5
X40 Sensor-Hub für Raspberry Pi 5

Ein modulares Framework zur dynamischen Auslesung und Visualisierung von Sensordaten aus dem Joy-IT X40-Sensorkit. Dieses Projekt wurde als Schulprojekt entwickelt und ist speziell für die Nutzung mit einem Touchscreen am Raspberry Pi 5 optimiert.
✨ Features

    Dynamisches Dashboard: Sensoren können zur Laufzeit über die GUI ausgewählt und konfiguriert werden.

    Touch-Optimiert: Große Bedienflächen und intuitive Menüführung ohne tiefe Untermenüs.

    Integrierter Anschluss-Guide: Die Software zeigt direkt an, welcher Sensor an welchen Pin (GPIO oder ADC) angeschlossen werden muss.

    Echtzeit-Performance: Dank Multithreading bleibt die GUI jederzeit flüssig, während die Sensordaten im Hintergrund verarbeitet werden.

    Hardware-Abstraktion: Einfache Integration von digitalen und analogen Sensoren (via ADS1115 ADC).

🛠 Technische Details

    Sprache: Python

    GUI-Library: Tkinter

    Hardware: Raspberry Pi 5, ADS1115 (KY-053) Analog-Digital-Wandler.

    Besonderheit: Anpassung an die neue Raspberry Pi 5 Architektur (RP1-Controller) durch Nutzung der adafruit-circuitpython-ads1x15 Bibliotheken.

🚀 Installation & Start

    Repository klonen.

    Es wird empfohlen, eine virtuelle Umgebung zu nutzen:
    Bash

    python -m venv venv
    source venv/bin/activate  # Unter Windows: venv\Scripts\activate

    Benötigte Bibliotheken installieren (z.B. gpiozero, adafruit-circuitpython-ads1x15).

    Programm starten:
    Bash

    python Main.py
    ``` [cite: 55]
