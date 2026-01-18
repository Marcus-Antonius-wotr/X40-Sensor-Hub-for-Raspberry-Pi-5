# Main.py
import tkinter as tk
import sys
import threading
from System_Config import config
from sensors import create_sensor
from Main_GUI import SensorDashboardGUI
from input_service import _update_loop # Importiert den Background-Dienst

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X40 Sensor System")
        
        # GUI_SCALE aus der Config laden
        self.scale = getattr(config, "GUI_SCALE", 1.0)
        
        # Fenstergröße basierend auf Skalierung berechnen
        width = int(1280 * 1)
        height = int(720 * 1)

        if sys.platform != "win32":
            self.attributes('-fullscreen', True)
        else:
            self.geometry(f"{width}x{height}")
            
        self.configure(bg=config.THEME["bg_main"])
        
        self.active_sensors = []
        
        # Startet den ADC-Hintergrunddienst (KY-053 Überwachung)
        threading.Thread(target=_update_loop, daemon=True).start()
        
        # GUI initialisieren
        self.gui = SensorDashboardGUI(self, self.init_hardware)
        self.gui.pack(fill="both", expand=True)
        
        # Hardware laden
        self.init_hardware()
        
        # Startseite anzeigen
        self.gui.show_page("OVERVIEW")
        
        # Update-Loop für Sensorwerte
        self.update_loop()

    def rebuild_ui(self):
        # Wird aufgerufen, wenn Skalierung oder Sensor-Anzahl geändert wurde
        self.gui.destroy()
        # Skalierung neu laden, falls sie in den Settings geändert wurde
        self.scale = getattr(config, "GUI_SCALE", 1.0)
        if sys.platform == "win32":
            self.geometry(f"{int(1280 * 1)}x{int(720 * 1)}")
            
        self.gui = SensorDashboardGUI(self, self.init_hardware)
        self.gui.pack(fill="both", expand=True)
        self.init_hardware()
        self.gui.show_page("OVERVIEW")

    def init_hardware(self):
        # Erstellt die Sensor-Objekte basierend auf der SENSOR_LIBRARY
        for s in self.active_sensors:
            if s: s.close()
            
        self.active_sensors = []
        num = getattr(config, "NUM_SENSORS", 3)
        for i in range(1, num + 1):
            stype = getattr(config, f"SLOT_{i}_TYPE", "Nicht belegt")
            spin = getattr(config, f"SLOT_{i}_PIN", 0)
            self.active_sensors.append(create_sensor(stype, spin))

    def update_loop(self):
        # Regelmäßiges Update der Anzeige in der Übersicht.
        if self.gui.current_page == "OVERVIEW" and hasattr(self.gui, 'val_labels'):
            for i, sensor in enumerate(self.active_sensors):
                if i < len(self.gui.val_labels):
                    val = sensor.read() if sensor else "OFFLINE"
                    
                    # Logik für Status-Farben
                    is_active = any(word in str(val).upper() for word in ["AN", "BEWEGUNG", "OK"])
                    color = config.THEME["accent"] if is_active else config.THEME["text_main"]
                    if "OFFLINE" in str(val): color = "gray"
                    
                    self.gui.val_labels[i].config(text=val, fg=color)
        
        # Intervall aus Config nutzen
        self.after(int(config.GUI_UPDATE_TIME * 1000), self.update_loop)

if __name__ == "__main__":
    app = App()
    app.mainloop()