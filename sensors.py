# sensors.py
import sys
import time
import threading
import glob
from System_Config import config
from sensor_calc_Profiles import SensorCalcProfiles

try:
    from gpiozero import Button, InputDevice, OutputDevice
    import board
    import busio
    import adafruit_dht
    import adafruit_bmp280
    HAS_HARDWARE = sys.platform != "win32"
except ImportError:
    HAS_HARDWARE = False

# Globale ADC-Werte (vom input_service befüllt)
adc_cache = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
adc_lock = threading.Lock()

class SensorBase:
    # Bauplan für alle Sensoren
    def __init__(self, pin_oder_kanal): 
        self.pin_oder_kanal = int(pin_oder_kanal)
    def read(self): return "N/A"
    def close(self): pass

class RealDigitalSensor(SensorBase):
    # Einfache An/Aus Sensoren
    def __init__(self, pin):
        super().__init__(pin)
        self.device = None
        if HAS_HARDWARE:
            try: self.device = Button(pin, pull_up=True)
            except: self.device = None
    def read(self):
        if not self.device: return "OFFLINE"
        return "AN" if self.device.is_pressed else "AUS"

class RealAnalogSensor(SensorBase):
    # Analoge Sensoren (input_service aktualiesiert adc_cache)
    def __init__(self, kanal, sensor_typ):
        super().__init__(kanal)
        self.sensor_typ = sensor_typ
    def read(self):
        with adc_lock: # Verhindert Chaos, wenn gleichzeitig gelesen und geschrieben wird
            spannung = adc_cache.get(self.pin_oder_kanal, 0.0)
        return SensorCalcProfiles.get_value(self.sensor_typ, spannung)


# --- SPEZIAL SENSOREN ---

class RealI2CSensor(SensorBase):
    # Für BMP280 (I2C Bus) 
    def __init__(self, typ):
        super().__init__(0)
        self.sensor = None
        if HAS_HARDWARE:
            try:
                i2c_bus = busio.I2C(board.SCL, board.SDA)
                if "BMP280" in typ:
                    # Der BMP280 hat zwei mögliche Adressen, wir testen beide durch
                    try:
                        self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_bus, address=0x77)
                    except ValueError:
                        try:
                            self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_bus, address=0x76)
                        except Exception as e:
                            print(f"BMP280 nicht gefunden: {e}")
                            self.sensor = None
            except Exception as e:
                print(f"I2C Bus Fehler: {e}")
                self.sensor = None
    def read(self):
        # Der Sensor ist ein kleiner Computer wir fragen einfach "Gib mir mal deine aktuelle Werte(aber flott)"
        if not self.sensor: return "I2C ERROR"
        try:
            return f"{self.sensor.temperature:.1f}°C {self.sensor.pressure:.0f}hPa"
        except: return "Fehler"

# --- Sensor Produktion ---

def create_sensor(sensor_typ, pin_oder_kanal):
    # Guckt in der Liste nach, was der Sensor braucht
    if sensor_typ == "Nicht belegt": return None
    
    sensor_info = config.SENSOR_LIBRARY.get(sensor_typ, {})
    modus = sensor_info.get("mode", "DIGITAL")

    # Welche Sensor Klasse soll es sein
    if modus == "ANALOG":
        return RealAnalogSensor(pin_oder_kanal, sensor_typ)
    elif modus == "DIGITAL":
        return RealDigitalSensor(pin_oder_kanal)
    elif modus == "I2C":
        return RealI2CSensor(sensor_typ)
    
    return None