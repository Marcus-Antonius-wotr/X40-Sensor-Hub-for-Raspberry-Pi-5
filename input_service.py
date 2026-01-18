# input_service.py
import threading
import time
import random
import math
from System_Config import config
from sensors import HAS_HARDWARE, adc_cache, adc_lock

def _update_loop():
    # Hier wird geguckt, ob der ADC (ADS1115) angeschlossen ist und funktioniert
    ads = None
    channels = []
    
    if HAS_HARDWARE and not getattr(config, "SIMULATION_ACTIVE", False):
        try:
            import board, busio
            from adafruit_ads1x15.ads1115 import ADS1115
            from adafruit_ads1x15.analog_in import AnalogIn
            
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS1115(i2c)
            
            # Erstellen der Kanäle direkt mit der AnalogIn-Klasse!!!
            channels = [
                AnalogIn(ads, 0), 
                AnalogIn(ads, 1), 
                AnalogIn(ads, 2), 
                AnalogIn(ads, 3)  
            ]
            print("ADS1115 erfolgreich initialisiert.")
        except Exception as e:
            print(f"Hardware-Init fehlgeschlagen: {e}")
            ads = None


    start_time = time.time()

    while True:
        if getattr(config, "SIMULATION_ACTIVE", False):
            # --- SIMULATIONS-MODUS ---
            elapsed = time.time() - start_time
            with adc_lock:
                # Wir erzeugen künstliche Wellenformen, um die GUI zu testen
                adc_cache[0] = 1.5 + math.sin(elapsed * 0.5) * 0.5
                adc_cache[1] = 1.0 + math.sin(elapsed * 2.0) * 0.2
                adc_cache[2] = random.uniform(0.5, 2.5)
                adc_cache[3] = 3.3 + random.uniform(-0.01, 0.01)
        
        elif ads:
            # --- ECHTER HARDWARE-MODUS ---
            for i in range(4):
                try:
                    val = channels[i].voltage
                    with adc_lock: # Stoppen der Chaos Götter
                        adc_cache[i] = val
                except: pass
        
        time.sleep(0.2)