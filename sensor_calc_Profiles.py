# sensor_calc_Profiles.py
import math

class SensorCalcProfiles:
    @staticmethod
    def get_value(stype, voltage):
        if stype == "Nicht belegt" or voltage is None:
            return "---"

        # Zuordnung der Sensoren zu ihren Formeln
        profiles = {
            "KY-013 Analog Temp":  SensorCalcProfiles._temp_ky013,
            "KY-048 Temp":     SensorCalcProfiles._temp_ky013,
            "KY-048 Mag":     SensorCalcProfiles._mag_hall,
            "KY-018 Fotowiderstand": SensorCalcProfiles._light_ky018,
            "KY-026 Flammen":      SensorCalcProfiles._fire_ky026,
            "KY-024 Linear-Hall":  SensorCalcProfiles._mag_hall,
            "KY-035 Analog-Hall":  SensorCalcProfiles._mag_hall,
            "KY-036 Metal-Touch":  SensorCalcProfiles._touch_ky036,
            "KY-037 Mikro Groß":   SensorCalcProfiles._sound_mic,
            "KY-038 Mikro Klein":  SensorCalcProfiles._sound_mic,
            "KY-039 Herzschlag":   SensorCalcProfiles._heart_ky039
        }

        func = profiles.get(stype)
        if func:
            return func(voltage)
        return f"{voltage:.2f} V"

    # --- EINZELNE BERECHNUNGSPROFILE ---

    @staticmethod
    def _temp_ky013(v):
        # Analoger Temperatur-Sensor (NTC Thermistor)
        if v < 0.1 or v > 3.2: return "Fehler"
        try:
            # Annahme: 10k Pull-Up Widerstand an 3.3V
            res = (10000 * v) / (3.3 - v)
            # Steinhart-Hart Näherung KI sacht beste methode für den sensor
            temp = 1 / (1 / (273.15 + 25) + math.log(res / 10000) / 3950)
            return f"{temp - 273.15:.1f} °C"
        except: return "N/A"

    @staticmethod
    def _light_ky018(v):
        # Fotowiderstand (LDR) - 0% ist dunkel, 100% ist hell
        percent = max(0, min(100, (1 - (v / 3.3)) * 100))
        return f"{percent:.1f} % Licht"

    @staticmethod
    def _fire_ky026(v):
        # Flammen-Sensor (Infrarot-Diode)
        if v < 0.8: return "ALARM: FEUER"
        if v < 2.0: return "Hitzequelle"
        return "Sicher"

    @staticmethod
    def _mag_hall(v):
        # Hallsensoren (Magnetfeld)
        # Nullpunkt bei 1.65V (halbe VCC)
        strength = v - 1.65
        unit = "mT" 
        prefix = "Süd" if strength > 0.05 else "Nord" if strength < -0.05 else "Neutral"
        return f"{prefix} ({abs(strength):.2f} {unit})"

    @staticmethod
    def _touch_ky036(v):
        # Reagiert auf Kapazitätsänderung / Hautwiderstand
        if v < 1.0: return "BERÜHRUNG!"
        return "Kein Kontakt"

    @staticmethod
    def _sound_mic(v):
        # Mikrofon-Module (Schallpegel)
        # Berechnet, wie stark der Schall von der normalen Spannung abweicht.
        diff = abs(v - 1.65)
        level = (diff / 1.65) * 100
        if level > 15: return f"Lärm ({level:.1f} %)"
        return f"Ruhig ({level:.1f} %)"

    @staticmethod
    def _heart_ky039(v):
        # Herzschlag-Sensor (Infrarot-Lichtschranke für den Finger)
        # Dieser Sensor liefert sehr feine Schwankungen.
        if 1.5 < v < 1.8: return "Puls..."
        return "Finger auflegen"

        # Standardfall: Spannung anzeigen
        return f"{voltage:.2f} V"