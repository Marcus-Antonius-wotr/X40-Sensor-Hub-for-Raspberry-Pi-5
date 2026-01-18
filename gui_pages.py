# gui_pages.py
import tkinter as tk
from tkinter import messagebox
from System_Config import config

class PageRenderer:
    def __init__(self, gui_context):
        self.gui_context = gui_context
        # Temporäre Speicher für die Slot-Konfiguration während der Bearbeitung
        self.temp_settings = {"type": None, "pin": None, "category": None}

    # --- Hilfsmethoden für einheitliches UI-Design ---
    def add_title(self, title_text):
        tk.Label(self.gui_context.content_frame, text=title_text.upper(), 
                 font=("Arial", self.gui_context.scale_value(18), "bold"), 
                 fg=config.THEME["text_main"], bg=config.THEME["bg_main"]).pack(anchor="w", pady=(0, 20))

    def create_settings_row(self, parent_container, label_text, widget_type, data_variable, **kwargs):
        # Baut eine wiederverwenbare Zeile für Einstellungen (z.B. Stepper oder Schalter)
        row_frame = tk.Frame(parent_container, bg=parent_container["bg"])
        row_frame.pack(fill="x", pady=self.gui_context.scale_value(5))
        
        tk.Label(row_frame, text=label_text, bg=parent_container["bg"], fg="white", 
                 font=("Arial", self.gui_context.scale_value(10))).pack(side="left")
        
        if widget_type == "stepper":
            tk.Button(row_frame, text="+", 
                      command=lambda: data_variable.set(round(min(kwargs['max_val'], data_variable.get() + kwargs['step_size']), 2))).pack(side="right")
            tk.Label(row_frame, textvariable=data_variable, width=6, fg=config.THEME["accent"], 
                     bg=parent_container["bg"], font=("Arial", 11, "bold")).pack(side="right")
            tk.Button(row_frame, text="-", 
                      command=lambda: data_variable.set(round(max(kwargs['min_val'], data_variable.get() - kwargs['step_size']), 2))).pack(side="right")
        
        elif widget_type == "toggle":
            def toggle_action(): 
                data_variable.set(not data_variable.get())
                status_text = "AN" if data_variable.get() else "AUS"
                bg_color = config.THEME["accent"] if data_variable.get() else "gray30"
                toggle_btn.config(text=status_text, bg=bg_color)
                
            toggle_btn = tk.Button(row_frame, text="AN" if data_variable.get() else "AUS", 
                                   command=toggle_action, width=8, 
                                   bg=config.THEME["accent"] if data_variable.get() else "gray30", fg="white")
            toggle_btn.pack(side="right")

    # --- Die einzelnen Seiten-Inhalte ---
    def draw_overview(self):
        # Zeichnet die Haupt-Übersicht mit den Sensor-Werten
        self.add_title("Live-Monitor")
        self.gui_context.val_labels = []
        
        for i in range(1, config.NUM_SENSORS + 1):
            slot_frame = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_sidebar"], pady=15, padx=20)
            slot_frame.pack(fill="x", pady=5)
            
            sensor_type = getattr(config, f"SLOT_{i}_TYPE")
            tk.Label(slot_frame, text=f"SLOT {i}: {sensor_type}", fg=config.THEME["text_dim"], 
                     bg=config.THEME["bg_sidebar"]).pack(side="left")
            
            value_label = tk.Label(slot_frame, text="Warte...", font=("Arial", 18, "bold"), 
                                   fg=config.THEME["accent"], bg=config.THEME["bg_sidebar"])
            value_label.pack(side="right")
            self.gui_context.val_labels.append(value_label)

    def draw_adc_monitor(self):
        # Zeigt die rohen Spannungswerte des KY-053 ADC
        self.add_title("ADC Rohwerte (KY-053)")
        grid_frame = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_main"])
        grid_frame.pack(fill="x")
        
        self.gui_context.adc_labels = []
        for i in range(4):
            channel_frame = tk.Frame(grid_frame, bg=config.THEME["bg_sidebar"], padx=15, pady=15)
            channel_frame.pack(side="left", expand=True, fill="both", padx=5)
            
            tk.Label(channel_frame, text=f"CH {i}", bg=config.THEME["bg_sidebar"], fg=config.THEME["text_dim"]).pack()
            volt_label = tk.Label(channel_frame, text="0.00V", bg=config.THEME["bg_sidebar"], 
                                  fg="white", font=("Arial", 14, "bold"))
            volt_label.pack()
            self.gui_context.adc_labels.append(volt_label)
            
        self.gui_context._update_adc_preview()

    def draw_general_settings(self):
        # Seite für globale Systemeinstellungen. 
        self.add_title("System-Konfiguration")
        settings_box = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_sidebar"], pady=25, padx=25)
        settings_box.pack(fill="x")
        
        # Lokale Variablen für das Formular
        count_var = tk.IntVar(value=config.NUM_SENSORS)
        scale_var = tk.DoubleVar(value=config.GUI_SCALE)
        sim_var = tk.BooleanVar(value=config.SIMULATION_ACTIVE)
        
        self.create_settings_row(settings_box, "ANZAHL AKTIVER SLOTS:", "stepper", count_var, min_val=1, max_val=5, step_size=1)
        self.create_settings_row(settings_box, "OBERFLÄCHEN SKALIERUNG:", "stepper", scale_var, min_val=0.5, max_val=2.0, step_size=0.1)
        self.create_settings_row(settings_box, "SIMULATOR-MODUS:", "toggle", sim_var)

        tk.Button(self.gui_context.content_frame, text="EINSTELLUNGEN ÜBERNEHMEN", bg=config.THEME["button_save"], 
                  font=("Arial", 10, "bold"), pady=12, 
                  command=lambda: self._save_general_settings(count_var, scale_var, sim_var)).pack(fill="x", pady=20)

    def draw_slot_settings(self, slot_number):
        # Detailseite zur Konfiguration eines einzelnen Sensors
        self.add_title(f"Sensor in Slot {slot_number} wählen")
        
        # Aktuelle Werte aus der Config in den temporären Speicher laden
        current_type = getattr(config, f"SLOT_{slot_number}_TYPE")
        self.temp_settings["type"] = tk.StringVar(value=current_type)
        self.temp_settings["pin"] = tk.StringVar(value=getattr(config, f"SLOT_{slot_number}_PIN"))
        
        # Passende Kategorie für den aktuellen Sensor finden
        current_category = "ANALOG"
        for cat_name, sensor_list in config.SENSOR_CATEGORIES.items():
            if current_type in sensor_list: 
                current_category = cat_name
                break
        self.temp_settings["category"] = tk.StringVar(value=current_category)

        # UI-Container vorbereiten
        self.category_bar = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_main"])
        self.category_bar.pack(fill="x", pady=10)
        
        self.sensor_grid = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_main"])
        self.sensor_grid.pack(fill="both", expand=True)

        self.hardware_pin_area = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_sidebar"], pady=15, padx=20)
        self.hardware_pin_area.pack(fill="x", side="bottom")

        # Buttons für Kategorien erzeugen
        for cat_name in [name for name in config.SENSOR_CATEGORIES.keys() if name != "NONE"]:
            tk.Button(self.category_bar, text=cat_name, font=("Arial", 8, "bold"),
                      command=lambda c=cat_name: self._switch_category(slot_number, c)).pack(side="left", padx=2)

        tk.Button(self.gui_context.content_frame, text="SLOT-KONFIGURATION SPEICHERN", bg=config.THEME["button_save"], 
                  font=("Arial", 10, "bold"), pady=10, 
                  command=lambda: self._save_slot_config(slot_number)).pack(fill="x", side="bottom", pady=5)

        self._refresh_sensor_grid(slot_number)

    def _switch_category(self, slot_id, new_category):
        self.temp_settings["category"].set(new_category)
        self._refresh_sensor_grid(slot_id)

    def _refresh_sensor_grid(self, slot_id):
        # Zeichnet die Buttons für die Sensor-Auswahl neu.
        for widget in self.sensor_grid.winfo_children(): 
            widget.destroy()
            
        current_cat = self.temp_settings["category"].get()
        sensor_lib = config.SENSOR_LIBRARY
        
        # Liste der Sensoren (inklusive "Nicht belegt")
        available_sensors = ["Nicht belegt"] + [name for name, info in sensor_lib.items() if info["cat"] == current_cat]
        
        for index, sensor_name in enumerate(available_sensors):
            is_selected = (sensor_name == self.temp_settings["type"].get())
            tk.Button(self.sensor_grid, text=sensor_name, width=20, height=2, bd=0,
                      bg=config.THEME["accent"] if is_selected else config.THEME["bg_button"],
                      fg="white" if is_selected else "gray80",
                      command=lambda name=sensor_name: self._select_sensor_type(slot_id, name)).grid(row=index//3, column=index%3, padx=2, pady=2)
        
        self._refresh_pin_selection_menu()

    def _select_sensor_type(self, slot_id, chosen_name):
        self.temp_settings["type"].set(chosen_name)
        self._refresh_sensor_grid(slot_id)

    def _refresh_pin_selection_menu(self):
        # Aktualisiert das Dropdown-Menü für die Pins
        for widget in self.hardware_pin_area.winfo_children(): 
            widget.destroy()
            
        current_type = self.temp_settings["type"].get()
        sensor_mode = config.SENSOR_LIBRARY.get(current_type, {"mode":"DIGITAL"})["mode"]
        
        # Pin-Optionen festlegen (Sperren von System-Pins für I2C/Serial)
        if sensor_mode == "ANALOG": 
            pin_options = [0, 1, 2, 3]
        elif sensor_mode == "ONEWIRE": 
            pin_options = [4]
        elif sensor_mode == "I2C":
            pin_options = ["I2C Bus (GPIO2/3)"]
            
        else: 
            gesperrte_pins = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15]
            pin_options = [p for p in range(28) if p not in gesperrte_pins] 
        
        if self.temp_settings["pin"].get() not in pin_options: 
            self.temp_settings["pin"].set(pin_options[0])
        
        tk.Label(self.hardware_pin_area, text="HARDWARE PIN / KANAL:", bg=config.THEME["bg_sidebar"], 
                 fg="white", font=("Arial", 10, "bold")).pack(side="left")
        
        tk.OptionMenu(self.hardware_pin_area, self.temp_settings["pin"], *pin_options).pack(side="right")

    def _save_general_settings(self, count_var, scale_var, sim_var):
        # Schreibt die globalen Settings zurück in die Config-Instanz. 
        config.NUM_SENSORS = count_var.get()
        config.GUI_SCALE = scale_var.get()
        config.SIMULATION_ACTIVE = sim_var.get()
        config.save_settings()
        messagebox.showinfo("Erfolg", "System-Einstellungen wurden lokal gesichert.")

    def _save_slot_config(self, slot_id):
        selected_type = self.temp_settings["type"].get()
        selected_pin_raw = self.temp_settings["pin"].get()
    
        if "I2C" in selected_pin_raw or "Bus" in selected_pin_raw:
            # Intern sind I2C-Geräte immer pin 0
            pin_value = 0 
        else:
            try:
                pin_value = int(selected_pin_raw)
            except (ValueError, tk.TclError):
                pin_value = 0

        # Werte in die Config schreiben
        setattr(config, f"SLOT_{slot_id}_TYPE", selected_type)
        setattr(config, f"SLOT_{slot_id}_PIN", pin_value)
    
        # Speichern und Hardware-Refresh
        config.save_settings()
        self.gui_context.refresh_hardware()
    
        messagebox.showinfo("Erfolg", f"Slot {slot_id} konfiguriert.")
        self.gui_context.show_page("OVERVIEW")

    # --- SEITE SCHALTPLAN ---
    def draw_wiring_guide(self):
        # Erzeugt eine Übersicht, wo die Sensoren angeschlossen werden
        self.add_title("Anschlussplan für Pi 5")
        
        # Container für die Tabelle
        tabelle = tk.Frame(self.gui_context.content_frame, bg=config.THEME["bg_sidebar"], padx=20, pady=20)
        tabelle.pack(fill="both", expand=True)

        # Spalten-Überschriften
        spalten = ["SLOT", "SENSOR-MODELL", "ANSCHLUSS / PIN", "INFO"]
        for spalten_index, text in enumerate(spalten):
            tk.Label(tabelle, text=text, bg=config.THEME["bg_sidebar"], fg=config.THEME["accent"], 
                     font=("Arial", 10, "bold")).grid(row=0, column=spalten_index, padx=15, pady=10, sticky="w")

        # Datenzeilen für jeden aktiven Slot
        for i in range(1, config.NUM_SENSORS + 1):
            s_typ = getattr(config, f"SLOT_{i}_TYPE")
            s_pin = getattr(config, f"SLOT_{i}_PIN")
            s_info = config.SENSOR_LIBRARY.get(s_typ, {"mode": "DIGITAL"})
            modus = s_info["mode"]
            
            # Fehlerprüfung und Texte
            hinweis = "Direkt an Pi"
            pin_text = f"GPIO {s_pin}"

            if s_typ == "Nicht belegt":
                pin_text, hinweis = "---", "Kein Kabel"
            elif modus == "ANALOG":
                pin_text, hinweis = f"ADC Kanal {s_pin}", "An KY-053 (I2C)"
            elif modus == "I2C" or s_typ == "KY-052 BMP280":
                pin_text, hinweis = "SDA (GPIO2) / SCL (GPIO3)", "I2C-Bus nutzen"
            elif "Ultraschall" in s_typ:
                hinweis = "Kombi-Pin (Trig/Echo)"
            elif modus == "ONEWIRE":
                hinweis = "4.7k Pull-Up nötig"

            # Die Zeile in die GUI schreiben
            zeilen_daten = [f"Slot {i}", s_typ, pin_text, hinweis]
            for spalten_index, inhalt in enumerate(zeilen_daten):
                tk.Label(tabelle, text=inhalt, bg=config.THEME["bg_sidebar"], fg="white",
                         font=("Arial", 10)).grid(row=i, column=spalten_index, padx=15, pady=8, sticky="w")

        # Hilfs-Anzeige für die Grundversorgung unten drunter
        strom_info = tk.Frame(self.gui_context.content_frame, bg="gray20", pady=15)
        strom_info.pack(fill="x", pady=20)
        
        info_text = "HINWEIS: Alle Sensoren benötigen zusätzlich 3.3V (VCC) und GND (Masse) vom Raspberry Pi."
        tk.Label(strom_info, text=info_text, fg="orange", bg="gray20", font=("Arial", 9, "italic")).pack()