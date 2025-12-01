import customtkinter as ctk
from ..theme_manager import get_color
import pandas as pd
import numbers
from backend.DAOs.CuentasDAO import CuentaDAO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinancialEcommercePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero de Ecommerce", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827")
        title.pack(side="left")
        
        # Header Buttons
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color=get_color('success')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Interpretar", command=self.show_interpretations, fg_color=get_color('accent')).pack(side="left", padx=6)
        
        # --- Pestañas ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#F97316", segmented_button_selected_hover_color="#D97706")
        self.tabview.pack(fill="both", expand=True)
        
        self.tabs = {
            "Cuentas": self.tabview.add("Cuentas"),
            "Balance": self.tabview.add("Balance General"),
            "Resultados": self.tabview.add("Estado de Resultados"),
            "Origen": self.tabview.add("Origen y Aplicación"),
            "Razones": self.tabview.add("Razones Financieras"),
            "Graficos": self.tabview.add("Gráficos"),
            "Proforma": self.tabview.add("Proforma")
        }
        
        # Estado inicial vacío para pestañas no implementadas
        for tab_name, tab in self.tabs.items():
            if tab_name in ["Resultados", "Balance", "Origen", "Razones", "Graficos"]:
                continue
            ctk.CTkLabel(tab, text=f"Contenido de {tab_name} en construcción", text_color="#374151").pack(pady=20)

        # Cargar datos
        self.load_income_statement()
        self.load_balance_sheet()
        self.load_cash_flow()
        self.load_ratios()
        self.load_charts()

    def load_balance_sheet(self):
        # 1. Datos del Período Anterior (Hardcoded)
        prev_data_raw = [
            {"Cuenta": "ACTIVOS", "Monto": None}, # Header
            {"Cuenta": "Efectivo", "Monto": 0},
            {"Cuenta": "Mobiliario y accesorios", "Monto": 36000},
            {"Cuenta": "Vehículos", "Monto": 50000},
            {"Cuenta": "Depreciación de mobiliario y accesorios", "Monto": 0},
            {"Cuenta": "Depreciación de vehículos", "Monto": 0},
            {"Cuenta": "Total Activos", "Monto": 86000},
            {"Cuenta": "PASIVOS", "Monto": None}, # Header
            {"Cuenta": "Total Pasivos", "Monto": 0},
            {"Cuenta": "CAPITAL", "Monto": None}, # Header
            {"Cuenta": "Capital Social", "Monto": 86000},
            {"Cuenta": "Utilidades Retenidas", "Monto": 0},
            {"Cuenta": "Total Capital", "Monto": 86000},
            {"Cuenta": "Total Pasivo + Capital", "Monto": 86000},
            {"Cuenta": "Diferencia", "Monto": 0}
        ]

        # Calcular Vertical % (Base = Total Activos = 86000)
        total_activos_prev = 86000
        for row in prev_data_raw:
            if row["Monto"] is not None:
                row["Vertical %"] = (row["Monto"] / total_activos_prev * 100) if total_activos_prev else 0.0
            else:
                row["Vertical %"] = None

        df_prev = pd.DataFrame(prev_data_raw)

        # 2. Datos del Período Actual (Desde BD)
        current_accounts = CuentaDAO.obtener_cuentas_balance_plataforma()
        
        curr_data_map = {}
        curr_activos = 0
        curr_pasivos = 0
        curr_capital = 0
        
        # Clasificación simple basada en IDs o nombres (Heurística)
        # Tipos: 1,2 = Activo? 5 = Capital? 
        # Nombres: 'Efectivo', 'Mobiliario', 'Vehiculos' -> Activos
        # 'Capital social', 'Utilidades retenidas' -> Capital
        # 'Renta', 'Gasto' -> No deberían estar aquí (son Resultados)
        
        for acc in current_accounts:
            name = acc.nombre_cuenta
            val = float(acc.saldo_actual)
            curr_data_map[name] = val
            
            # Sumar a totales (simplificado por nombre/tipo)
            # Asumimos que la BD tiene los tipos correctos.
            # Ajuste manual para totales basado en nombres conocidos
            if name in ["Efectivo", "Mobiliario y accesorios", "Vehiculos", "Vehículos"]:
                curr_activos += val
            elif "Depreciacion" in name or "Depreciación" in name:
                 # Depreciaciones suelen restar, pero si vienen positivas en BD, hay que ver.
                 # En el ejemplo del usuario, se restan: 0 + 36000 + 50000 - 0 - 0
                 # Asumiremos que se restan si son depreciaciones
                 curr_activos -= val 
            elif name in ["Capital social", "Utilidades retenidas"]:
                curr_capital += val
            # Pasivos?
        
        # Totales calculados
        curr_pasivo_mas_capital = curr_pasivos + curr_capital
        curr_diferencia = curr_activos - curr_pasivo_mas_capital

        # Mapear a estructura
        curr_data_list = []
        
        # Usar estructura de prev para orden
        for row in prev_data_raw:
            key = row["Cuenta"]
            
            if key in ["ACTIVOS", "PASIVOS", "CAPITAL"]: # Headers
                curr_data_list.append({"Cuenta": key, "Monto": None, "Vertical %": None})
                continue
                
            # Totales calculados
            if key == "Total Activos":
                val = curr_activos
            elif key == "Total Pasivos":
                val = curr_pasivos
            elif key == "Total Capital":
                val = curr_capital
            elif key == "Total Pasivo + Capital":
                val = curr_pasivo_mas_capital
            elif key == "Diferencia":
                val = curr_diferencia
            else:
                # Cuentas individuales
                # Normalizar keys - buscar con case-insensitive
                lookup_key = key
                val = 0.0
                
                # Intentar búsqueda exacta primero
                if key in curr_data_map:
                    val = curr_data_map[key]
                else:
                    # Intentar variaciones comunes
                    if key == "Vehículos" and "Vehiculos" in curr_data_map:
                        val = curr_data_map["Vehiculos"]
                    elif "Depreciación" in key:
                        simple = key.replace("Depreciación", "Depreciacion")
                        val = curr_data_map.get(simple, 0.0)
                    else:
                        # Búsqueda case-insensitive
                        key_lower = key.lower()
                        for db_key, db_val in curr_data_map.items():
                            if db_key.lower() == key_lower:
                                val = db_val
                                break

            vert = (val / curr_activos * 100) if (curr_activos and val is not None) else 0.0
            if val is None: vert = None
            
            curr_data_list.append({"Cuenta": key, "Monto": val, "Vertical %": vert})

        df_curr = pd.DataFrame(curr_data_list)

        # 3. Renderizar UI
        tab = self.tabs["Balance"]
        for widget in tab.winfo_children():
            widget.destroy()

        # Contenedor principal
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame Izquierdo (Anterior)
        left_frame = ctk.CTkFrame(container, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left_frame, text="Período Anterior", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', pady=(0, 5))
        self.render_table(left_frame, df_prev)

        # Frame Derecho (Actual)
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(right_frame, text="Período Actual", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', pady=(0, 5))
        self.render_table(right_frame, df_curr)
        
        # 4. Análisis Horizontal (Abajo)
        horizontal_data = []
        for i in range(len(prev_data_raw)):
            row_prev = prev_data_raw[i]
            row_curr = curr_data_list[i]
            
            key = row_prev["Cuenta"]
            val_prev = row_prev["Monto"]
            val_curr = row_curr["Monto"]
            
            if val_prev is None or val_curr is None:
                continue # Skip headers
                
            var_abs = val_curr - val_prev
            var_pct = (var_abs / val_prev * 100) if val_prev != 0 else 0.0
            
            horizontal_data.append({
                "Cuenta": key,
                "Año Base": val_prev,
                "Año Actual": val_curr,
                "Variación $": var_abs,
                "Variación %": var_pct
            })
            
        df_horizontal = pd.DataFrame(horizontal_data)
        ctk.CTkLabel(tab, text="Análisis Horizontal (Variación)", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', padx=10, pady=(20, 5))
        self.render_table(tab, df_horizontal)

    def load_cash_flow(self):
        """Calculate and display Sources and Uses (Cash Flow Statement)"""
        # We need the balance sheet data from both periods
        # Reuse the data structures from load_balance_sheet
        
        # Previous period data
        prev_data_raw = [
            {"Cuenta": "ACTIVOS", "Monto": None, "Tipo": "Header"},
            {"Cuenta": "Efectivo", "Monto": 0, "Tipo": "Activo"},
            {"Cuenta": "Mobiliario y accesorios", "Monto": 36000, "Tipo": "Activo"},
            {"Cuenta": "Vehículos", "Monto": 50000, "Tipo": "Activo"},
            {"Cuenta": "Depreciación de mobiliario y accesorios", "Monto": 0, "Tipo": "Activo"},
            {"Cuenta": "Depreciación de vehículos", "Monto": 0, "Tipo": "Activo"},
            {"Cuenta": "PASIVOS", "Monto": None, "Tipo": "Header"},
            {"Cuenta": "CAPITAL", "Monto": None, "Tipo": "Header"},
            {"Cuenta": "Capital Social", "Monto": 86000, "Tipo": "Capital"},
            {"Cuenta": "Utilidades Retenidas", "Monto": 0, "Tipo": "Capital"}
        ]
        
        # Current period data (fetch from DB)
        current_accounts = CuentaDAO.obtener_cuentas_balance_plataforma()
        curr_data_map = {}
        
        for acc in current_accounts:
            name = acc.nombre_cuenta
            val = float(acc.saldo_actual)
            tipo = None
            
            # Classify by type
            if name in ["Efectivo", "Mobiliario y accesorios", "Vehiculos", "Vehículos"] or "Depreciacion" in name or "Depreciación" in name:
                tipo = "Activo"
            elif name in ["Capital social", "Utilidades retenidas"]:
                tipo = "Capital"
            else:
                tipo = "Pasivo"  # Default for unknown
                
            curr_data_map[name] = {"Monto": val, "Tipo": tipo}
        
        # Calculate Sources and Uses
        sources = []
        uses = []
        
        for row in prev_data_raw:
            cuenta = row["Cuenta"]
            monto_prev = row["Monto"]
            tipo = row["Tipo"]
            
            if monto_prev is None or tipo == "Header":
                continue
                
            # Find current value (with improved matching)
            monto_curr = 0.0
            tipo_curr = tipo
            
            # Helper function to normalize account names
            def normalize_name(name):
                """Remove accents and normalize for comparison"""
                import unicodedata
                # Remove accents
                normalized = unicodedata.normalize('NFD', name)
                normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
                return normalized.lower().strip()
            
            # Try exact match first
            if cuenta in curr_data_map:
                monto_curr = curr_data_map[cuenta]["Monto"]
                tipo_curr = curr_data_map[cuenta]["Tipo"]
            else:
                # Try normalized matching (handles accents, case, etc.)
                cuenta_normalized = normalize_name(cuenta)
                for db_key, db_data in curr_data_map.items():
                    if normalize_name(db_key) == cuenta_normalized:
                        monto_curr = db_data["Monto"]
                        tipo_curr = db_data["Tipo"]
                        break
            
            diff = monto_curr - monto_prev
            
            if diff == 0 or abs(diff) < 0.01:  # Skip if no change (with small tolerance for floating point)
                continue
                
            # Sources and Uses logic:
            # - Asset decrease = Source
            # - Asset increase = Use
            # - Liability/Capital increase = Source
            # - Liability/Capital decrease = Use
            
            if tipo_curr == "Activo":
                if diff < 0:
                    sources.append({"Cuenta": cuenta, "Monto": abs(diff)})
                elif diff > 0:
                    uses.append({"Cuenta": cuenta, "Monto": abs(diff)})
            else:  # Pasivo or Capital
                if diff > 0:
                    sources.append({"Cuenta": cuenta, "Monto": abs(diff)})
                elif diff < 0:
                    uses.append({"Cuenta": cuenta, "Monto": abs(diff)})
        
        # Create DataFrames
        df_sources = pd.DataFrame(sources) if sources else pd.DataFrame(columns=["Cuenta", "Monto"])
        df_uses = pd.DataFrame(uses) if uses else pd.DataFrame(columns=["Cuenta", "Monto"])
        
        # Render UI (side-by-side like in financial.py)
        tab = self.tabs["Origen"]
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Sources frame (left)
        sources_frame = ctk.CTkScrollableFrame(tab, label_text="Fuentes", fg_color=get_color('card_bg'))
        sources_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)
        
        if not df_sources.empty:
            for _, row in df_sources.iterrows():
                ctk.CTkLabel(sources_frame, text=f"{row['Cuenta']}: ${row['Monto']:,.2f}", text_color="#374151").pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(sources_frame, text="No hay fuentes de efectivo", text_color="#9CA3AF").pack(pady=10)
        
        # Uses frame (right)
        uses_frame = ctk.CTkScrollableFrame(tab, label_text="Usos", fg_color=get_color('card_bg'))
        uses_frame.pack(side="right", fill="both", expand=True, padx=5, pady=10)
        
        if not df_uses.empty:
            for _, row in df_uses.iterrows():
                ctk.CTkLabel(uses_frame, text=f"{row['Cuenta']}: ${row['Monto']:,.2f}", text_color="#374151").pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(uses_frame, text="No hay usos de efectivo", text_color="#9CA3AF").pack(pady=10)

    def load_ratios(self):
        """Calculate and display financial ratios for both periods"""
        # Fetch current period data
        balance_accounts = CuentaDAO.obtener_cuentas_balance_plataforma()
        income_accounts = CuentaDAO.obtener_cuentas_resultados_plataforma()
        
        # Helper to get account value by name
        def get_account_value(accounts_list, account_name):
            import unicodedata
            def normalize(name):
                normalized = unicodedata.normalize('NFD', name)
                normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
                return normalized.lower().strip()
            
            target_normalized = normalize(account_name)
            for acc in accounts_list:
                if normalize(acc.nombre_cuenta) == target_normalized:
                    return float(acc.saldo_actual)
            return 0.0
        
        # Calculate totals for CURRENT period
        curr_activos = 0
        curr_pasivos = 0
        curr_capital = 0
        
        for acc in balance_accounts:
            val = float(acc.saldo_actual)
            if acc.id_tipo_cuenta in [1, 2]:  # Activos
                curr_activos += val
            elif acc.id_tipo_cuenta in [3, 4]:  # Pasivos
                curr_pasivos += val
            elif acc.id_tipo_cuenta == 5:  # Capital
                curr_capital += val
        
        curr_ingresos = sum(float(acc.saldo_actual) for acc in income_accounts if acc.id_tipo_cuenta == 6)
        curr_gastos = sum(float(acc.saldo_actual) for acc in income_accounts if acc.id_tipo_cuenta == 7)
        curr_utilidad = curr_ingresos - curr_gastos
        
        # Get specific accounts for current period
        curr_inventarios = get_account_value(balance_accounts, "Inventarios")
        curr_cxc = get_account_value(balance_accounts, "Cuentas por Cobrar")
        
        # PREVIOUS period totals (hardcoded)
        prev_activos = 86000
        prev_pasivos = 0
        prev_capital = 86000
        prev_ingresos = 12800
        prev_gastos = 12800
        prev_utilidad = 0
        prev_inventarios = 0
        prev_cxc = 0
        
        # Safe division helper
        def safe_div(a, b):
            try:
                return (a / b) if b not in (0, None) else None
            except:
                return None
        
        # Calculate all ratios for BOTH periods
        ratios_data = []
        
        # 1. Liquidez Corriente
        ratios_data.append({
            "Ratio": "Liquidez Corriente",
            "Año Base": safe_div(prev_activos, prev_pasivos) if prev_pasivos else None,
            "Año Actual": safe_div(curr_activos, curr_pasivos) if curr_pasivos else None
        })
        
        # 2. Prueba Ácida
        ratios_data.append({
            "Ratio": "Prueba Ácida",
            "Año Base": safe_div(prev_activos - prev_inventarios, prev_pasivos) if prev_pasivos else None,
            "Año Actual": safe_div(curr_activos - curr_inventarios, curr_pasivos) if curr_pasivos else None
        })
        
        # 3. Capital de Trabajo
        ratios_data.append({
            "Ratio": "Capital de Trabajo",
            "Año Base": prev_activos - prev_pasivos,
            "Año Actual": curr_activos - curr_pasivos
        })
        
        # 4. CNO (Capital Neto de Trabajo Operativo)
        # CNO = Activos Corrientes Operativos - Pasivos Corrientes Operativos
        # Para simplificar, usamos: CNO = (Activos - Efectivo) - Pasivos
        prev_efectivo = 0  # From previous period data
        curr_efectivo = get_account_value(balance_accounts, "Efectivo")
        
        ratios_data.append({
            "Ratio": "CNO (Capital Neto de Trabajo Operativo)",
            "Año Base": (prev_activos - prev_efectivo) - prev_pasivos,
            "Año Actual": (curr_activos - curr_efectivo) - curr_pasivos
        })
        
        # 5. Rotación de Inventarios
        ratios_data.append({
            "Ratio": "Rotación de Inventarios",
            "Año Base": safe_div(prev_gastos, prev_inventarios) if prev_inventarios else None,
            "Año Actual": safe_div(curr_gastos, curr_inventarios) if curr_inventarios else None
        })
        
        # 5. Periodo Promedio de Cobro
        ratios_data.append({
            "Ratio": "Periodo Promedio de Cobro (días)",
            "Año Base": (safe_div(prev_cxc, prev_ingresos) * 365) if prev_ingresos and prev_cxc else None,
            "Año Actual": (safe_div(curr_cxc, curr_ingresos) * 365) if curr_ingresos and curr_cxc else None
        })
        
        # 6. Rotación de Activos Totales
        ratios_data.append({
            "Ratio": "Rotación de Activos Totales",
            "Año Base": safe_div(prev_ingresos, prev_activos),
            "Año Actual": safe_div(curr_ingresos, curr_activos)
        })
        
        # 7. Índice de Endeudamiento
        ratios_data.append({
            "Ratio": "Índice de Endeudamiento (Pasivo/Activo)",
            "Año Base": safe_div(prev_pasivos, prev_activos),
            "Año Actual": safe_div(curr_pasivos, curr_activos)
        })
        
        # 8. Margen de Utilidad Bruta
        ratios_data.append({
            "Ratio": "Margen de Utilidad Bruta",
            "Año Base": safe_div(prev_ingresos - prev_gastos, prev_ingresos),
            "Año Actual": safe_div(curr_ingresos - curr_gastos, curr_ingresos)
        })
        
        # 9. Margen de Utilidad Operativa (same as bruta for simplified model)
        ratios_data.append({
            "Ratio": "Margen de Utilidad Operativa",
            "Año Base": safe_div(prev_utilidad, prev_ingresos),
            "Año Actual": safe_div(curr_utilidad, curr_ingresos)
        })
        
        # 10. Margen de Utilidad Neta
        ratios_data.append({
            "Ratio": "Margen de Utilidad Neta",
            "Año Base": safe_div(prev_utilidad, prev_ingresos),
            "Año Actual": safe_div(curr_utilidad, curr_ingresos)
        })
        
        # 11. ROA
        ratios_data.append({
            "Ratio": "ROA (Rent. sobre Activos)",
            "Año Base": safe_div(prev_utilidad, prev_activos),
            "Año Actual": safe_div(curr_utilidad, curr_activos)
        })
        
        # 12. ROE
        ratios_data.append({
            "Ratio": "ROE (Rent. sobre Patrimonio)",
            "Año Base": safe_div(prev_utilidad, prev_capital),
            "Año Actual": safe_div(curr_utilidad, curr_capital)
        })
        
        # 13. Cobertura de Intereses (EBIT/Intereses) - N/A for this model
        ratios_data.append({
            "Ratio": "Cobertura de Intereses (EBIT/Intereses)",
            "Año Base": None,
            "Año Actual": None
        })
        
        # 14. DuPont 3 pasos
        prev_margen = safe_div(prev_utilidad, prev_ingresos)
        prev_rot = safe_div(prev_ingresos, prev_activos)
        prev_mult = safe_div(prev_activos, prev_capital)
        prev_dupont3 = None
        if all(x is not None for x in [prev_margen, prev_rot, prev_mult]):
            prev_dupont3 = prev_margen * prev_rot * prev_mult
        
        curr_margen = safe_div(curr_utilidad, curr_ingresos)
        curr_rot = safe_div(curr_ingresos, curr_activos)
        curr_mult = safe_div(curr_activos, curr_capital)
        curr_dupont3 = None
        if all(x is not None for x in [curr_margen, curr_rot, curr_mult]):
            curr_dupont3 = curr_margen * curr_rot * curr_mult
        
        ratios_data.append({
            "Ratio": "DuPont (3 pasos) - ROE",
            "Año Base": prev_dupont3,
            "Año Actual": curr_dupont3
        })
        
        # 15. DuPont 5 pasos - N/A for simplified model
        ratios_data.append({
            "Ratio": "DuPont (5 pasos) - ROE Extendido",
            "Año Base": None,
            "Año Actual": None
        })
        
        # Calculate change percentage
        for ratio in ratios_data:
            base = ratio["Año Base"]
            curr = ratio["Año Actual"]
            if base is not None and curr is not None and base != 0:
                ratio["Cambio %"] = ((curr - base) / abs(base)) * 100
            else:
                ratio["Cambio %"] = None
        
        df_ratios = pd.DataFrame(ratios_data)
        
        # Render UI
        tab = self.tabs["Razones"]
        for widget in tab.winfo_children():
            widget.destroy()
        
        sf = ctk.CTkScrollableFrame(tab)
        sf.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkFrame(sf, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(header, text="Razón", font=ctk.CTkFont(weight="bold"), width=300, anchor="w").pack(side="left")
        ctk.CTkLabel(header, text="Año Base", font=ctk.CTkFont(weight="bold"), width=150).pack(side="left")
        ctk.CTkLabel(header, text="Año Actual", font=ctk.CTkFont(weight="bold"), width=150).pack(side="left")
        ctk.CTkLabel(header, text="Cambio %", font=ctk.CTkFont(weight="bold"), width=120).pack(side="left")
        
        # Rows
        for _, row in df_ratios.iterrows():
            name = row["Ratio"]
            base = row["Año Base"]
            curr = row["Año Actual"]
            change = row["Cambio %"]
            
            rframe = ctk.CTkFrame(sf, fg_color=get_color('card_bg'))
            rframe.pack(fill="x", pady=4, padx=2)
            
            # Ratio name
            ctk.CTkLabel(rframe, text=name, width=300, anchor="w", font=ctk.CTkFont(weight="bold"), text_color="#1f2937").pack(side="left", padx=(6, 0))
            
            # Format values
            def format_ratio(val, ratio_name):
                if val is None:
                    return "-"
                # Check for NaN or infinity
                try:
                    import math
                    if math.isnan(val) or math.isinf(val):
                        return "-"
                except:
                    pass
                # Show as percentage for certain ratios
                if any(k in ratio_name.lower() for k in ['margen', 'roa', 'roe', 'endeudamiento', 'dupont']):
                    return f"{val * 100:.2f}%"
                # Show as days
                if 'días' in ratio_name.lower():
                    return f"{val:.0f} días"
                # Show as currency for Capital de Trabajo and CNO
                if 'capital de trabajo' in ratio_name.lower() or 'cno' in ratio_name.lower():
                    return f"${val:,.2f}"
                return f"{val:.2f}"

            
            ctk.CTkLabel(rframe, text=format_ratio(base, name), width=150, anchor="center").pack(side="left")
            ctk.CTkLabel(rframe, text=format_ratio(curr, name), width=150, anchor="center").pack(side="left")
            
            # Change % with color
            if change is None:
                change_text = "-"
                color = "#374151"
            else:
                sign = '+' if change >= 0 else ''
                change_text = f"{sign}{change:.2f}%"
                color = "#16a34a" if change >= 0 else "#dc2626"
            
            ctk.CTkLabel(rframe, text=change_text, width=120, anchor="center", text_color=color, font=ctk.CTkFont(weight="bold")).pack(side="left")

    def load_charts(self):
        """Display charts: pie charts for asset/liability breakdown and bar chart for comparison"""
        # Fetch current period data
        balance_accounts = CuentaDAO.obtener_cuentas_balance_plataforma()
        
        # Helper to normalize names
        import unicodedata
        def normalize_name(name):
            normalized = unicodedata.normalize('NFD', name)
            normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
            return normalized.lower().strip()
        
        # Organize current period accounts
        activos_data = {}
        pasivos_data = {}
        capital_data = {}
        
        for acc in balance_accounts:
            name = acc.nombre_cuenta
            val = float(acc.saldo_actual)
            
            if acc.id_tipo_cuenta in [1, 2]:  # Activos
                activos_data[name] = val
            elif acc.id_tipo_cuenta in [3, 4]:  # Pasivos
                pasivos_data[name] = val
            elif acc.id_tipo_cuenta == 5:  # Capital
                capital_data[name] = val
        
        # Calculate totals
        total_activos_curr = sum(activos_data.values())
        total_pasivos_curr = sum(pasivos_data.values())
        total_capital_curr = sum(capital_data.values())
        
        # Previous period totals
        total_activos_prev = 86000
        
        # Clear tab
        tab = self.tabs["Graficos"]
        for widget in tab.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top container for pie charts (side by side)
        top_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # === PIE CHART 1: ACTIVOS ===
        fig1, ax1 = plt.subplots(figsize=(5, 4.5))
        
        if activos_data:
            # Filter out very small values and group them as "Otros"
            threshold = total_activos_curr * 0.03  # 3% threshold
            main_items = {}
            otros_total = 0
            
            for name, val in activos_data.items():
                if val >= threshold:
                    main_items[name] = val
                else:
                    otros_total += val
            
            if otros_total > 0:
                main_items['Otros'] = otros_total
            
            labels1 = list(main_items.keys())
            sizes1 = list(main_items.values())
            colors1 = plt.cm.Set3(range(len(labels1)))
            
            # Use autopct only, no labels on the pie itself
            wedges, texts, autotexts = ax1.pie(sizes1, autopct='%1.1f%%', startangle=90, colors=colors1)
            
            # Make percentage text bold and white
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            # Add legend outside the pie
            ax1.legend(wedges, labels1, title="Cuentas", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
            ax1.set_title('Composición de Activos\nPeríodo Actual', fontsize=13, fontweight='bold', pad=20)
        else:
            ax1.text(0.5, 0.5, 'No hay datos de activos', ha='center', va='center')
            ax1.set_title('Composición de Activos\nPeríodo Actual', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=top_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", padx=10)
        
        # === PIE CHART 2: PASIVOS + CAPITAL ===
        fig2, ax2 = plt.subplots(figsize=(5, 4.5))
        
        # Combine pasivos and capital
        pasivo_capital_data = {}
        pasivo_capital_data.update(pasivos_data)
        pasivo_capital_data.update(capital_data)
        
        total_pasivo_capital = total_pasivos_curr + total_capital_curr
        
        if pasivo_capital_data:
            # Filter small values
            threshold2 = total_pasivo_capital * 0.03 if total_pasivo_capital > 0 else 0
            main_items2 = {}
            otros_total2 = 0
            
            for name, val in pasivo_capital_data.items():
                if val >= threshold2:
                    main_items2[name] = val
                else:
                    otros_total2 += val
            
            if otros_total2 > 0:
                main_items2['Otros'] = otros_total2
            
            labels2 = list(main_items2.keys())
            sizes2 = list(main_items2.values())
            colors2 = plt.cm.Set2(range(len(labels2)))
            
            wedges2, texts2, autotexts2 = ax2.pie(sizes2, autopct='%1.1f%%', startangle=90, colors=colors2)
            
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            ax2.legend(wedges2, labels2, title="Cuentas", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
            ax2.set_title('Composición de Pasivos + Capital\nPeríodo Actual', fontsize=13, fontweight='bold', pad=20)
        else:
            ax2.text(0.5, 0.5, 'No hay datos de pasivos/capital', ha='center', va='center')
            ax2.set_title('Composición de Pasivos + Capital\nPeríodo Actual', fontsize=13, fontweight='bold', pad=20)
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=top_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="left", padx=10)
        
        # === BAR CHART: COMPARISON ===
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        
        periods = ['Período Anterior', 'Período Actual']
        values = [total_activos_prev, total_activos_curr]
        colors3 = ['#E5E7EB', '#06B6D4']
        
        bars = ax3.bar(periods, values, color=colors3, width=0.6)
        ax3.set_title('Comparación de Activos Totales', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Monto (C$)', fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax3.grid(axis='y', alpha=0.3)
        
        canvas3 = FigureCanvasTkAgg(fig3, master=scroll_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(pady=10)


    def load_income_statement(self):
        # 1. Datos del Período Anterior (Hardcoded)
        prev_data_raw = [
            {"Cuenta": "Ingresos", "Monto": 12800},
            {"Cuenta": "Gasto de envío", "Monto": 2800},
            {"Cuenta": "Renta", "Monto": 10000},
            {"Cuenta": "Utilidad Antes de IR", "Monto": 3000},
            {"Cuenta": "IR", "Monto": 0},
            {"Cuenta": "Utilidad del período", "Monto": 0}
        ]
        
        # Calcular Vertical % para Anterior
        prev_ingresos = 12800
        for row in prev_data_raw:
            row["Vertical %"] = (row["Monto"] / prev_ingresos * 100) if prev_ingresos else 0.0
            
        df_prev = pd.DataFrame(prev_data_raw)
        
        # 2. Datos del Período Actual (Desde BD)
        current_accounts = CuentaDAO.obtener_cuentas_resultados_plataforma()
        
        # Agrupar y calcular totales para el período actual
        curr_ingresos = 0
        curr_gastos = 0
        curr_data_map = {}
        
        for acc in current_accounts:
            name = acc.nombre_cuenta
            val = float(acc.saldo_actual)
            curr_data_map[name] = val
            
            if acc.id_tipo_cuenta == 6: # Ingresos
                curr_ingresos += val
            elif acc.id_tipo_cuenta == 7: # Gastos
                curr_gastos += val

        # Calcular utilidades actuales
        curr_util_antes_ir = curr_ingresos - curr_gastos
        curr_ir = 0 
        curr_util_neta = curr_util_antes_ir - curr_ir

        # Agregar totales calculados
        curr_data_map["Ingresos"] = curr_ingresos
        if "Gasto de envio" in curr_data_map:
            curr_data_map["Gasto de envío"] = curr_data_map.pop("Gasto de envio")
        
        curr_data_map["Utilidad Antes de IR"] = curr_util_antes_ir
        curr_data_map["IR"] = curr_ir
        curr_data_map["Utilidad del período"] = curr_util_neta

        # Construir lista para DataFrame Actual (ordenado similar al anterior si es posible)
        curr_data_list = []
        processed_keys = set()
        
        # Primero las cuentas que coinciden con el orden del anterior
        for row in prev_data_raw:
            key = row["Cuenta"]
            if key in curr_data_map:
                val = curr_data_map[key]
                vert = (val / curr_ingresos * 100) if curr_ingresos else 0.0
                curr_data_list.append({"Cuenta": key, "Monto": val, "Vertical %": vert})
                processed_keys.add(key)
        
        # Luego el resto de cuentas
        for key, val in curr_data_map.items():
            if key not in processed_keys:
                vert = (val / curr_ingresos * 100) if curr_ingresos else 0.0
                curr_data_list.append({"Cuenta": key, "Monto": val, "Vertical %": vert})

        df_curr = pd.DataFrame(curr_data_list)
        
        # 3. Renderizar UI (Dos tablas lado a lado)
        tab = self.tabs["Resultados"]
        for widget in tab.winfo_children():
            widget.destroy()

        # Contenedor principal
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame Izquierdo (Anterior)
        left_frame = ctk.CTkFrame(container, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Período Anterior", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', pady=(0, 5))
        self.render_table(left_frame, df_prev)
        
        # Frame Derecho (Actual)
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(right_frame, text="Período Actual", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', pady=(0, 5))
        self.render_table(right_frame, df_curr)

        # 4. Análisis Horizontal (Abajo)
        horizontal_data = []
        
        # Crear un mapa del anterior para búsqueda rápida
        prev_map = {row["Cuenta"]: row["Monto"] for row in prev_data_raw}
        
        # Unir todas las claves
        all_keys = sorted(list(set(prev_map.keys()) | set(curr_data_map.keys())))
        
        # Ordenar: Ingresos primero, luego gastos, luego utilidades
        # (Una heurística simple o usar el orden de prev_data_raw + nuevos)
        ordered_keys = []
        # Primero los que estaban en prev (mantiene orden lógico)
        for row in prev_data_raw:
            if row["Cuenta"] in all_keys:
                ordered_keys.append(row["Cuenta"])
        # Luego los nuevos
        for k in all_keys:
            if k not in ordered_keys:
                ordered_keys.append(k)

        for key in ordered_keys:
            val_prev = prev_map.get(key, 0.0)
            val_curr = curr_data_map.get(key, 0.0)
            var_abs = val_curr - val_prev
            var_pct = (var_abs / val_prev * 100) if val_prev != 0 else 0.0
            
            horizontal_data.append({
                "Cuenta": key,
                "Año Base": val_prev,
                "Año Actual": val_curr,
                "Variación $": var_abs,
                "Variación %": var_pct
            })
            
        df_horizontal = pd.DataFrame(horizontal_data)
        
        ctk.CTkLabel(tab, text="Análisis Horizontal (Variación)", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(anchor='w', padx=10, pady=(20, 5))
        self.render_table(tab, df_horizontal)

    def render_table(self, parent, df):
        if df is None or df.empty: return
        
        sf = ctk.CTkScrollableFrame(parent)
        sf.pack(fill="both", expand=True)
        
        # Headers
        headers = list(df.columns)
        for col, header in enumerate(headers):
            ctk.CTkLabel(sf, text=header, font=ctk.CTkFont(weight="bold"), text_color="#111827").grid(row=0, column=col, padx=8, pady=6)
            
        # Rows
        for r, row in df.iterrows():
            for c, col in enumerate(headers):
                header_name = headers[c]
                val = row[col]

                # Handle missing
                if val is None or pd.isna(val):
                    display = '-'
                else:
                    # Numeric formatting
                    if isinstance(val, numbers.Number):
                        # Percentage columns
                        if ('%' in header_name) or ('Vertical' in header_name):
                            display = f"{val:.2f}%"
                        # Currency / accounting format for monto-like fields
                        elif ('Saldo' in header_name) or ('Monto' in header_name):
                            try:
                                num = float(val)
                                if num < 0:
                                    display = f"(${abs(num):,.2f})"
                                else:
                                    display = f"${num:,.2f}"
                            except Exception:
                                display = str(val)
                        else:
                            display = str(val)
                    else:
                        display = str(val)

                ctk.CTkLabel(sf, text=display, text_color="#374151").grid(row=r+1, column=c, padx=8, pady=4)

    def export_report(self):
        print("Exportar Reporte clicked")

    def show_interpretations(self):
        print("Interpretar clicked")
