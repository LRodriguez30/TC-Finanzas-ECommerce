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
        
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero Avanzado", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Descargar Plantillas", command=self.download_templates, fg_color="#D1D5DB", text_color="black", hover_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Importar Año Base", command=lambda: self.import_data('base'), fg_color="#F97316", hover_color="#D97706").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Importar Año Actual", command=lambda: self.import_data('current'), fg_color="#F97316", hover_color="#D97706").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color="#65A30D", hover_color="#4d7c0f").pack(side="left", padx=5)

        # --- Tabs ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#F97316", segmented_button_selected_hover_color="#D97706")
        self.tabview.pack(fill="both", expand=True)
        
        self.tabs = {
            "Balance": self.tabview.add("Balance General"),
            "Resultados": self.tabview.add("Estado de Resultados"),
            "Origen": self.tabview.add("Origen y Aplicación"),
            "Razones": self.tabview.add("Razones Financieras"),
            "Graficos": self.tabview.add("Gráficos")
        }
        
        # Initial empty state
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
        
        # Load data (Simplified: assuming file has both sheets for now, or user uploads same file twice if split)
        # In a real app, we'd store paths and load when both are ready, or load partially.
        # Here we will try to load BS and IS from the selected file.
        bs, iss = self.excel_handler.load_financial_data(path)
        
        if year_type == 'base':
            self.analyzer.base_bs = bs
            self.analyzer.base_is = iss
            print("Datos Base cargados")
        else:
            self.analyzer.current_bs = bs
            self.analyzer.current_is = iss
            print("Datos Actuales cargados")
            
        # Trigger analysis if we have enough data (or partial)
        if self.analyzer.base_bs is not None and self.analyzer.current_bs is not None:
            self.analyzer.perform_analysis()
            self.refresh_ui()

    def refresh_ui(self):
        # Clear tabs
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

        # 4. Ratios (Placeholder for now)
        ctk.CTkLabel(self.tabs["Razones"], text="Cálculo de razones detallado aquí...", text_color="#854D0E").pack()

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
        # Example chart: Total Assets Base vs Current
        if self.analyzer.base_bs is None: return
        
        fig, ax = plt.subplots(figsize=(5, 4))
        # Sum of 'Monto' for Activo
        base_assets = self.analyzer.base_bs[self.analyzer.base_bs['Tipo'] == 'Activo']['Monto'].sum()
        curr_assets = self.analyzer.current_bs[self.analyzer.current_bs['Tipo'] == 'Activo']['Monto'].sum()
        
        ax.bar(['Año Base', 'Año Actual'], [base_assets, curr_assets], color=['#D1D5DB', '#F97316']) # Gray / Orange
        ax.set_title("Total Activos", color="#854D0E")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def export_report(self):
        print("Exporting report...")
        # Implementation would use pandas to write to Excel
