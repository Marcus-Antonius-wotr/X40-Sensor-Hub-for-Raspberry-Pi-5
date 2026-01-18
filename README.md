X40 Sensor Hub for Raspberry Pi 5

A modular framework for dynamic reading and visualization of sensor data from the Joy-IT X40 sensor kit. This project was developed as a school project and is specifically optimized for use with a touchscreen on the Raspberry Pi 5.

## ✨ Features
* **Dynamic Dashboard:** Sensors can be selected and configured at runtime via the GUI.
* **Touch-Optimized:** Large interactive areas and intuitive menu navigation without deep submenus.
* **Integrated Connection Guide:** The software directly displays which sensor needs to be connected to which pin (GPIO or ADC).
* **Real-time Performance:** Thanks to multithreading (background sensor thread), the GUI remains responsive at all times.
* **Hardware Abstraction:** Easy integration of digital and analog sensors via the ADS1115 ADC.
    
Note: The documentation and GUI are in German, but the source code is in English for better readability.

German:

Ein modulares Framework zur dynamischen Auslesung und Visualisierung von Sensordaten aus dem **Joy-IT X40-Sensorkit**. Dieses Projekt wurde als Schulprojekt entwickelt und ist gezielt für die Nutzung mit einem **Touchscreen** am Raspberry Pi 5 optimiert.

## ✨ Features
* **Dynamisches Dashboard:** Sensoren können zur Laufzeit über die GUI ausgewählt und konfiguriert werden.
* **Touch-Optimiert:** Große interaktive Flächen und intuitive Menüführung ohne verschachtelte Untermenüs.
* **Integrierter Anschluss-Guide:** Die Software zeigt direkt an, welcher Sensor an welchen Pin (GPIO oder ADC) angeschlossen werden muss.
* **Echtzeit-Performance:** Dank Multithreading (Hintergrund-Thread für Sensoren) bleibt die GUI jederzeit reaktionsfähig.
* **Hardware-Abstraktion:** Einfache Integration von digitalen und analogen Sensoren via ADS1115 ADC.

| Live-Monitor | Anschluss-Guide |
| :---: | :---: |
| <img src="docs/Oberview.jpg" width="400"> | <img src="docs/AnschlussPlan.jpg" width="400"> |

## 🛠 Technical Details (English)
* **Language:** Python
* **Architecture:** Modular layers (Presentation, Logic, Hardware) for easy extensibility.
* **Hardware:** Raspberry Pi 5, ADS1115 (KY-053) Analog-to-Digital Converter.
* **Special Feature:** Compatibility with the new RP1 I/O architecture of the Pi 5 by using modern CircuitPython libraries.
    
## 🛠 Technische Details
* **Sprache:** Python
* **Architektur:** Modulare Ebenen (Präsentation, Logik, Hardware) für leichte Erweiterbarkeit.
* **Hardware:** Raspberry Pi 5, ADS1115 (KY-053) Analog-Digital-Wandler.
* **Besonderheit:** Anpassung an die neue **RP1-I/O-Architektur** des Pi 5 durch Nutzung moderner CircuitPython-Bibliotheken.

## 🚀 Installation & Start
1. Repository klonen.
2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```
3. Benötigte Bibliotheken installieren:
```bash
pip install gpiozero adafruit-circuitpython-ads1x15
```
4. Wichtig: Stelle sicher, dass der I2C-Bus an deinem Raspberry Pi aktiviert ist
```bash
sudo raspi-config
```
5.Programm starten:
```bash
python Main.py
```
## 📝 Lizenz
Dieses Projekt steht unter der **MIT-Lizenz** – "Soll jeder machen, was er will!"
