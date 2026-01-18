# Main_GUI.py
import tkinter as tk
from System_Config import config
from gui_pages import PageRenderer

class SensorDashboardGUI(tk.Frame):
    def __init__(self, parent_container, hardware_refresh_callback):
        # Skalierung direkt aus der Config (wichtig für kleine/große Displays)
        self.scaling_factor = getattr(config, "GUI_SCALE", 1.0)
        
        super().__init__(parent_container, bg=config.THEME["bg_main"])
        self.refresh_hardware = hardware_refresh_callback
        self.current_page = None
        
        # Listen für die Update-Loops (vom Renderer befüllt)
        self.val_labels = []
        self.adc_labels = []
        
        # Der "Maler" für die Inhalte
        self.renderer = PageRenderer(self)
                
        # Linke Spalte: Navigation
        self.sidebar_frame = tk.Frame(self, width=self.scale_value(280), bg=config.THEME["bg_sidebar"])
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Rechte Spalte: Haupt-Anzeigebereich
        self.content_frame = tk.Frame(self, bg=config.THEME["bg_main"])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=self.scale_value(20), pady=self.scale_value(20))

        self.build_sidebar()

    def scale_value(self, base_pixel):
        # Rechnet Pixel-Werte passend zur Skalierung um. 
        return int(base_pixel * self.scaling_factor)

    def build_sidebar(self):
        # Baut das Hauptmenü in der linken Sidebar zusammen
        tk.Label(self.sidebar_frame, text="X40 SENSOR-HUB", fg=config.THEME["accent"], 
                 bg=config.THEME["bg_sidebar"], font=("Arial", self.scale_value(16), "bold"), 
                 pady=self.scale_value(30)).pack(fill="x")
        
        # Liste der Navigations-Punkte erstellen
        navigation_items = [("Übersicht", "OVERVIEW"), ("AD-Wandler", "ADC_SET"),("Schaltplan", "WIRING")]
        
        # Dynamisch Buttons für die konfigurierten Slots
        max_slots = getattr(config, "NUM_SENSORS", 3)
        for i in range(1, max_slots + 1):
            navigation_items.append((f"Slot {i}", f"S{i}"))
        
        navigation_items.append(("Allgemein", "GEN"))

        # Navigations-Buttons erstellen
        for button_text, page_identifier in navigation_items:
            tk.Button(self.sidebar_frame, text=button_text.upper(), bg=config.THEME["bg_button"], 
                      fg=config.THEME["text_main"], font=("Arial", self.scale_value(10), "bold"), 
                      bd=0, pady=self.scale_value(10), 
                      command=lambda pid=page_identifier: self.show_page(pid)).pack(fill="x", pady=1, padx=15)

    def show_page(self, page_id):
        # Wechselt die Ansicht und leert den alten Content-Bereich
        if self.current_page == page_id: 
            return
            
        self.current_page = page_id
        
        # Den aktuellen Inhalt im Content-Bereich entfernen
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()

        # Den Maler rufen, um die Seite zu zeichnen
        if page_id == "OVERVIEW": 
            self.renderer.draw_overview()
        elif page_id == "ADC_SET": 
            self.renderer.draw_adc_monitor()
        elif page_id == "WIRING":
            self.renderer.draw_wiring_guide()
        elif page_id.startswith("S"): 
            slot_number = page_id[1:]
            self.renderer.draw_slot_settings(slot_number)
        else: 
            self.renderer.draw_general_settings()

    def _update_adc_preview(self):
        # Aktualisiert die Spannungsanzeige im ADC-Monitor
        if self.current_page == "ADC_SET":
            from sensors import adc_cache, adc_lock
            with adc_lock:
                for index, label in enumerate(self.adc_labels):
                    if index < len(adc_cache):
                        label.config(text=f"{adc_cache[index]:.3f} V")
            
            self.after(200, self._update_adc_preview)