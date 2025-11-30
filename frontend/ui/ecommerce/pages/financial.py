import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import os
from backend.logic.financial_models import FinancialAnalyzer
from backend.logic.excel_handler import ExcelHandler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class FinancialPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.analyzer = FinancialAnalyzer()
        self.excel_handler = ExcelHandler()
        
        # --- Encabezado ---
        # Contenedor superior con título y botones de acciones (importar, exportar, plantillas)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero Avanzado", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")
        
        # Contenedor de botones
        # Botones para descargar plantillas, importar años y exportar reportes
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Descargar Plantillas", command=self.download_templates, fg_color="#D1D5DB", text_color="black", hover_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Importar Año Base", command=lambda: self.import_data('base'), fg_color="#F97316", hover_color="#D97706").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Importar Año Actual", command=lambda: self.import_data('current'), fg_color="#F97316", hover_color="#D97706").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color="#65A30D", hover_color="#4d7c0f").pack(side="left", padx=5)

        # --- Pestañas ---
        # Secciones del análisis financiero: Balance, Estado de Resultados, Fuentes/Usos, Razones y Gráficos
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#F97316", segmented_button_selected_hover_color="#D97706")
        self.tabview.pack(fill="both", expand=True)
        
        self.tabs = {
            "Balance": self.tabview.add("Balance General"),
            "Resultados": self.tabview.add("Estado de Resultados"),
            "Origen": self.tabview.add("Origen y Aplicación"),
            "Razones": self.tabview.add("Razones Financieras"),
            "Graficos": self.tabview.add("Gráficos")
        }
        
        # Estado inicial vacío
        # Muestra mensajes indicando que el usuario debe importar datos para ver resultados
        self.show_empty_state()

    def show_empty_state(self):
        for tab_name, tab in self.tabs.items():
            for widget in tab.winfo_children(): widget.destroy()
            ctk.CTkLabel(tab, text="Importe datos para ver el análisis.", text_color="#854D0E").pack(pady=20)

    def download_templates(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta para guardar plantillas")
        if path:
            self.excel_handler.generate_templates(path)
            print(f"Plantillas guardadas en {path}")

    def import_data(self, year_type):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path: return
        
        # Carga de datos (simplificado): asumimos que el archivo contiene ambas hojas necesarias
        # En una aplicación real gestionaríamos rutas, validaciones y cargas parciales por separado.
        # Aquí intentamos leer Balance (BS) y Estado de Resultados (IS) desde el archivo seleccionado.
        bs, iss = self.excel_handler.load_financial_data(path)
        
        if year_type == 'base':
            self.analyzer.base_bs = bs
            self.analyzer.base_is = iss
            print("Datos Base cargados")
        else:
            self.analyzer.current_bs = bs
            self.analyzer.current_is = iss
            print("Datos Actuales cargados")
            
        # Dispara el análisis si ya contamos con los datos mínimos requeridos
        # (por ejemplo si se han cargado tanto el año base como el actual)
        if self.analyzer.base_bs is not None and self.analyzer.current_bs is not None:
            self.analyzer.perform_analysis()
            self.refresh_ui()

    def refresh_ui(self):
        # Limpia el contenido anterior de cada pestaña antes de renderizar los nuevos resultados
        for tab in self.tabs.values():
            for widget in tab.winfo_children(): widget.destroy()
            
        # 1. Balance General Tab
        self.render_table(self.tabs["Balance"], self.analyzer.analysis_results.get('horizontal_bs'))
        
        # 2. Income Statement Tab
        self.render_table(self.tabs["Resultados"], self.analyzer.analysis_results.get('horizontal_is'))
        
        # 3. Sources and Uses
        su = self.analyzer.analysis_results.get('sources_uses')
        if su:
            f_frame = ctk.CTkScrollableFrame(self.tabs["Origen"], label_text="Fuentes")
            f_frame.pack(side="left", fill="both", expand=True, padx=5)
            self.render_simple_table(f_frame, su['Fuentes'])
            
            u_frame = ctk.CTkScrollableFrame(self.tabs["Origen"], label_text="Usos")
            u_frame.pack(side="right", fill="both", expand=True, padx=5)
            self.render_simple_table(u_frame, su['Usos'])

        # 4. Razones
        # Mostrar el DataFrame de razones calculadas por el analizador en una vista formateada
        ratios_df = self.analyzer.analysis_results.get('ratios')
        if ratios_df is not None and not ratios_df.empty:
            self.render_ratios(self.tabs["Razones"], ratios_df)
        else:
            ctk.CTkLabel(self.tabs["Razones"], text="No hay datos de razones disponibles. Importe ambos años.", text_color="#854D0E").pack(pady=10)

        # 5. Charts
        self.render_charts(self.tabs["Graficos"])

    def render_table(self, parent, df):
        if df is None or df.empty: return
        
        sf = ctk.CTkScrollableFrame(parent)
        sf.pack(fill="both", expand=True)
        
        # Headers
        headers = list(df.columns)
        for col, header in enumerate(headers):
            ctk.CTkLabel(sf, text=header, font=ctk.CTkFont(weight="bold"), text_color="#854D0E").grid(row=0, column=col, padx=5, pady=5)
            
        # Rows
        for r, row in df.iterrows():
            for c, col in enumerate(headers):
                val = row[col]
                if isinstance(val, float): val = f"{val:.2f}"
                ctk.CTkLabel(sf, text=str(val)).grid(row=r+1, column=c, padx=5, pady=2)

    def render_simple_table(self, parent, df):
        if df is None or df.empty: return
        for r, row in df.iterrows():
            ctk.CTkLabel(parent, text=f"{row['Cuenta']}: ${row['Monto']:.2f}").pack(anchor="w")

    def render_charts(self, parent):
        # Gráfico de ejemplo: Total de Activos Año Base vs Año Actual
        # Compara la suma de activos entre ambos años para una vista rápida de cambios
        if self.analyzer.base_bs is None: return
        
        fig, ax = plt.subplots(figsize=(5, 4))
        # Suma de la columna 'Monto' para las cuentas clasificadas como 'Activo'
        base_assets = self.analyzer.base_bs[self.analyzer.base_bs['Tipo'] == 'Activo']['Monto'].sum()
        curr_assets = self.analyzer.current_bs[self.analyzer.current_bs['Tipo'] == 'Activo']['Monto'].sum()
        
        ax.bar(['Año Base', 'Año Actual'], [base_assets, curr_assets], color=['#D1D5DB', '#F97316']) # Colores: gris / naranja para distinguir años
        ax.set_title("Total Activos", color="#854D0E")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def _format_value_for_display(self, val, ratio_name=None):
        # Formatea valores para mostrar: si es None devuelve '-' ; si está entre -1 y 1 y el nombre sugiere ratio -> porcentaje
        if val is None:
            return '-'
        try:
            v = float(val)
        except Exception:
            return str(val)

        # Heurística para mostrar como porcentaje
        lower_name = (ratio_name or '').lower()
        if any(k in lower_name for k in ['margin', 'roa', 'roe', 'return', 'ratio', 'turnover', 'rotat']):
            # mostrar como porcentaje cuando el valor esté en unidad (0.12 -> 12.00%)
            return f"{v*100:.2f}%" if abs(v) < 20 else f"{v:.2f}"

        # Si es un número grande, separador de miles
        if abs(v) >= 1000:
            return f"{v:,.2f}"
        return f"{v:.2f}"

    def render_ratios(self, parent, df):
        # Contenedor scrollable para las tarjetas de razones
        sf = ctk.CTkScrollableFrame(parent)
        sf.pack(fill="both", expand=True, padx=10, pady=10)

        # Encabezado de columnas (estético)
        header = ctk.CTkFrame(sf, fg_color="transparent")
        header.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(header, text="Razón", font=ctk.CTkFont(weight="bold"), width=200, anchor="w").pack(side="left")
        ctk.CTkLabel(header, text="Año Base", font=ctk.CTkFont(weight="bold"), width=150).pack(side="left")
        ctk.CTkLabel(header, text="Año Actual", font=ctk.CTkFont(weight="bold"), width=150).pack(side="left")
        ctk.CTkLabel(header, text="Cambio %", font=ctk.CTkFont(weight="bold"), width=120).pack(side="left")

        # Cada fila del DataFrame -> tarjeta/row
        for _, row in df.iterrows():
            name = row.get('Ratio', '')
            base = row.get('Año Base')
            curr = row.get('Año Actual')
            change = row.get('Cambio %')

            rframe = ctk.CTkFrame(sf, fg_color="#FFFFFF")
            rframe.pack(fill="x", pady=4, padx=2)

            # Nombre de la razón
            ctk.CTkLabel(rframe, text=name, width=200, anchor="w", font=ctk.CTkFont(weight="bold"), text_color="#1f2937").pack(side="left", padx=(6,0))

            # Valores base y actual
            ctk.CTkLabel(rframe, text=self._format_value_for_display(base, name), width=150, anchor="center").pack(side="left")
            ctk.CTkLabel(rframe, text=self._format_value_for_display(curr, name), width=150, anchor="center").pack(side="left")

            # Cambio % con color
            if change is None:
                change_text = '-'
                color = "#374151"
            else:
                try:
                    ch = float(change)
                    sign = '+' if ch >= 0 else ''
                    change_text = f"{sign}{ch:.2f}%"
                    color = "#16a34a" if ch >= 0 else "#dc2626"
                except Exception:
                    change_text = str(change)
                    color = "#374151"

            ctk.CTkLabel(rframe, text=change_text, width=120, anchor="e", text_color=color).pack(side="left", padx=(0,6))

    def export_report(self):
        print("Exporting report...")
        # La implementación real usaría pandas para generar un archivo Excel con el reporte
