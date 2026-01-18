# System_Config.py
import json
import os
import threading

class SystemConfig:
    _instance = None
    _lock = threading.Lock()
    
    # Standartwerte
    DEFAULTS = {
        "NUM_SENSORS": 3,
        "ADC_GAIN": 1,
        "ADC_SAMPLING": 128,
        "GUI_UPDATE_TIME": 0.5,
        "GUI_SCALE": 1.0,
        "SIMULATION_ACTIVE": False
    }

    # Farbschema (man könnte weitere definieren und in die einstellung zur auswahl geben)
    THEME = {
        "bg_main": "gray12",
        "bg_sidebar": "gray15",
        "bg_button": "gray20",
        "bg_button_hover":"gray25",
        "accent": "mediumpurple1",
        "button_save": "orange",
        "button_settings": "orange",
        "text_main": "gold2",
        "text_button": "gray10",
        "text_dim": "indianred1",

    }

    # Zentrale Datenbank für das Joy-IT X40 Kit
    SENSOR_LIBRARY = {           
    # --- LICHT / IR / TEMP ---
    "KY-010 Lichtschranke":{"mode": "DIGITAL", "cat": "LICHT/IR/TEMP"},
    "KY-022 IR-Empfänger": {"mode": "DIGITAL", "cat": "LICHT/IR/TEMP"},  
    "KY-028 Digital Temp": {"mode": "DIGITAL", "cat": "LICHT/IR/TEMP"},
    "KY-032 Hindernis":    {"mode": "DIGITAL", "cat": "LICHT/IR/TEMP"},
    "KY-033 Tracking":     {"mode": "DIGITAL", "cat": "LICHT/IR/TEMP"},
    
    # --- MECHANIK / MAGNET ---
    "KY-002 Erschütterung":{"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-003 Hall-Magnet":  {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-004 Taster":       {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-017 Neigung":      {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-020 Neigung sw.":  {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-021 Reed-Schalt.": {"mode": "DIGITAL", "cat": "MECHANIK"},        
    "KY-025 Reed Digital": {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-031 Klopfsensor":  {"mode": "DIGITAL", "cat": "MECHANIK"},
    "KY-040 Drehgeber":    {"mode": "ENCODER", "cat": "MECHANIK"},
            
    # --- ANALOGE SENSOREN ---
    "KY-013 Analog Temp":   {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-018 Fotowiderstand":{"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-024 Linear-Hall":   {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-026 Flammen":       {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-035 Analog-Hall":   {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-036 Metal-Touch":   {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-037 Mikro Groß":    {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-038 Mikro Klein":   {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-039 Herzschlag":    {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-048 Temp":          {"mode": "ANALOG",  "cat": "ANALOG"},
    "KY-048 Mag":           {"mode": "ANALOG",  "cat": "ANALOG"},

    # --- SPEZIAL PROTOKOLLE ---
    "KY-052 BMP280":       {"mode": "I2C",      "cat": "SPEZIAL"},

    # --- GLOBAL ---
    "Nicht belegt":        {"mode": "NONE",     "cat": "NONE"}
}

    def __new__(cls):
        # Das hier sorgt dafür, dass es die Konfiguration nur EINMAL im Speicher gibt (Singleton).
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SystemConfig, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized: return
        for key, value in self.DEFAULTS.items():
            setattr(self, key, value)
        
        # Standard-Pins für 5 Slots
        default_pins = [17, 27, 22, 23, 24]
        for i in range(1, 6):
            if not hasattr(self, f"SLOT_{i}_TYPE"):
                setattr(self, f"SLOT_{i}_TYPE", "Nicht belegt")
            if not hasattr(self, f"SLOT_{i}_PIN"):
                setattr(self, f"SLOT_{i}_PIN", default_pins[i-1])

        self.CONFIG_FILE = "sensor_config.json"
        self.load_settings()
        self._initialized = True

    def check_pin_conflicts(self):
        # Prüft, ob Pins doppelt belegt sind.
        used_pins = {}
        num = getattr(self, "NUM_SENSORS", 5)
        
        for i in range(1, num + 1):
            stype = getattr(self, f"SLOT_{i}_TYPE")
            if stype != "Nicht belegt":
                pin = getattr(self, f"SLOT_{i}_PIN")
                if pin in used_pins:
                    used_pins[pin].append(i)
                else:
                    used_pins[pin] = [i]
        
        conflicts = {pin: slots for pin, slots in used_pins.items() if len(slots) > 1}
        return conflicts if conflicts else None

    def save_settings(self):
        # Speichert die Einstellungen in die JSON Datei
        data = {k: getattr(self, k) for k in self.DEFAULTS}
        for i in range(1, 6):
            data[f"SLOT_{i}_TYPE"] = getattr(self, f"SLOT_{i}_TYPE")
            data[f"SLOT_{i}_PIN"] = getattr(self, f"SLOT_{i}_PIN")
            
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def load_settings(self):
        # Lädt die Einstellungen aus der JSON Datei
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        setattr(self, k, v)
            except:
                pass
        else:
            self.save_settings()

    # Hilfsmethode für die GUI, um die Kategorien für das Menü zu gruppieren
    @property
    def SENSOR_CATEGORIES(self):
        cats = {}
        for name, data in self.SENSOR_LIBRARY.items():
            c = data["cat"]
            if c not in cats: cats[c] = []
            cats[c].append(name)
        return cats

config = SystemConfig()