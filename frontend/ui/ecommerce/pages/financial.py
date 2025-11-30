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
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827")
        title.pack(side="left")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Descargar Plantillas", command=self.download_templates, fg_color="#E5E7EB", text_color="#111827").pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Importar Año Base", command=lambda: self.import_data('base'), fg_color="#06B6D4").pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Importar Año Actual", command=lambda: self.import_data('current'), fg_color="#06B6D4").pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color="#10B981").pack(side="left", padx=6)

        # --- Tabs ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#F97316", segmented_button_selected_hover_color="#D97706")
        self.tabview.pack(fill="both", expand=True)
        
        self.tabs = {
            "Balance": self.tabview.add("Balance General"),
            "Resultados": self.tabview.add("Estado de Resultados"),
            "Origen": self.tabview.add("Origen y Aplicación"),
            "Razones": self.tabview.add("Razones Financieras"),
            "Graficos": self.tabview.add("Gráficos"),
            "Proforma": self.tabview.add("Proforma")
        }
        
        # Initial empty state
        self.show_empty_state()

    def show_empty_state(self):
        for tab_name, tab in self.tabs.items():
            for widget in tab.winfo_children(): widget.destroy()
            ctk.CTkLabel(tab, text="Importe datos para ver el análisis.", text_color="#374151").pack(pady=20)

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

        # Trigger analysis when both base and current are available
        if self.analyzer.base_bs is not None and self.analyzer.current_bs is not None and self.analyzer.base_is is not None and self.analyzer.current_is is not None:
            self.analyzer.perform_analysis()
            self.refresh_ui()

    def refresh_ui(self):
        # Clear tabs
        for tab in self.tabs.values():
            for widget in tab.winfo_children(): widget.destroy()
            
        # 1. Balance General Tab -> mostrar Vertical (Base y Actual) y Horizontal con etiquetas
        btab = self.tabs["Balance"]
        vbs_base = self.analyzer.analysis_results.get('vertical_bs_base')
        vbs_actual = self.analyzer.analysis_results.get('vertical_bs_actual')
        hbs = self.analyzer.analysis_results.get('horizontal_bs')
        ctk.CTkLabel(btab, text="Análisis Vertical - Año Base (monto y % sobre Total Activos)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(6,2))
        self.render_table(btab, vbs_base)
        ctk.CTkLabel(btab, text="Análisis Vertical - Año Actual (monto y % sobre Total Activos)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(8,2))
        self.render_table(btab, vbs_actual)
        ctk.CTkLabel(btab, text="Análisis Horizontal (Año Base vs Año Actual)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(10,2))
        self.render_table(btab, hbs)

        # 2. Income Statement Tab -> Vertical y Horizontal
        itab = self.tabs["Resultados"]
        vis_base = self.analyzer.analysis_results.get('vertical_is_base')
        vis_actual = self.analyzer.analysis_results.get('vertical_is_actual')
        his = self.analyzer.analysis_results.get('horizontal_is')
        ctk.CTkLabel(itab, text="Análisis Vertical - Año Base (porcentaje sobre Ventas Netas)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(6,2))
        self.render_table(itab, vis_base)
        ctk.CTkLabel(itab, text="Análisis Vertical - Año Actual (porcentaje sobre Ventas Netas)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(8,2))
        self.render_table(itab, vis_actual)
        ctk.CTkLabel(itab, text="Análisis Horizontal (Año Base vs Año Actual)", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=8, pady=(10,2))
        self.render_table(itab, his)
        
        # 3. Sources and Uses
        su = self.analyzer.analysis_results.get('sources_uses')
        if su:
            f_frame = ctk.CTkScrollableFrame(self.tabs["Origen"], label_text="Fuentes")
            f_frame.pack(side="left", fill="both", expand=True, padx=5)
            self.render_simple_table(f_frame, su['Fuentes'])
            
            u_frame = ctk.CTkScrollableFrame(self.tabs["Origen"], label_text="Usos")
            u_frame.pack(side="right", fill="both", expand=True, padx=5)
            self.render_simple_table(u_frame, su['Usos'])

        # 4. Ratios
        self.render_ratios(self.tabs["Razones"])

        # 5. Charts
        self.render_charts(self.tabs["Graficos"])

        # 6. Proforma tab
        self.render_proforma(self.tabs["Proforma"])

    def render_table(self, parent, df):
        if df is None or df.empty: return
        
        sf = ctk.CTkScrollableFrame(parent)
        sf.pack(fill="both", expand=True)
        
        # Headers
        headers = list(df.columns)
        for col, header in enumerate(headers):
            ctk.CTkLabel(sf, text=header, font=ctk.CTkFont(weight="bold"), text_color="#111827").grid(row=0, column=col, padx=8, pady=6)
            
        # Rows
        import pandas as _pd
        import numbers

        for r, row in df.iterrows():
            for c, col in enumerate(headers):
                header_name = headers[c]
                val = row[col]

                # Handle missing
                if val is None or (_pd.isna(val) if hasattr(_pd, 'isna') else False):
                    display = '-'
                else:
                    # Numeric formatting
                    if isinstance(val, numbers.Number):
                        # Percentage columns
                        if ('%' in header_name) or ('Vertical' in header_name) or ('Variación %' in header_name) or ('% ' in header_name):
                            display = f"{val:.2f}%"
                        else:
                            # Currency / accounting format for monto-like fields
                            if ('Monto' in header_name) or ('Variación $' in header_name) or ('Valor' in header_name) or ('Capital' in header_name) or ('Saldo' in header_name):
                                # show with $ and parentheses for negatives
                                try:
                                    num = float(val)
                                    if num < 0:
                                        display = f"(${abs(num):,.2f})"
                                    else:
                                        display = f"${num:,.2f}"
                                except Exception:
                                    display = str(val)
                            else:
                                # generic numeric
                                try:
                                    num = float(val)
                                    display = f"{num:,.2f}"
                                except Exception:
                                    display = str(val)
                    else:
                        display = str(val)

                ctk.CTkLabel(sf, text=display, text_color="#374151").grid(row=r+1, column=c, padx=8, pady=4)

    def render_simple_table(self, parent, df):
        if df is None or df.empty: return
        for r, row in df.iterrows():
            ctk.CTkLabel(parent, text=f"{row['Cuenta']}: ${row['Monto']:.2f}", text_color="#374151").pack(anchor="w", pady=2)

    def render_charts(self, parent):
        # Example chart: Total Assets Base vs Current
        if self.analyzer.base_bs is None: return
        
        fig, ax = plt.subplots(figsize=(5, 4))
        # Sum of 'Monto' for Activo
        base_assets = self.analyzer.base_bs[self.analyzer.base_bs['Tipo'] == 'Activo']['Monto'].sum()
        curr_assets = self.analyzer.current_bs[self.analyzer.current_bs['Tipo'] == 'Activo']['Monto'].sum()
        ax.bar(['Año Base', 'Año Actual'], [base_assets, curr_assets], color=['#E5E7EB', '#06B6D4'])
        ax.set_title("Total Activos", color="#111827")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def export_report(self):
        print("Exporting report...")
        # Implementation would use pandas to write to Excel

    def render_proforma(self, parent):
        for w in parent.winfo_children():
            w.destroy()

        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.pack(fill='x', padx=8, pady=6)
        ctk.CTkLabel(top, text="Proforma - Proyección rápida", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(side='left')

        form = ctk.CTkFrame(parent)
        form.pack(fill='x', padx=8, pady=6)

        # Campos de porcentaje
        self.pct_entries = {}
        fields = [
            ('Crecimiento Ventas (%)', 'ventas'),
            ('Inventarios (%)', 'inventarios'),
            ('Cuentas por Cobrar (%)', 'cxc'),
            ('Activos Fijos (%)', 'activos_fijos'),
            ('Pasivos (%)', 'pasivos'),
            ('Patrimonio (%)', 'patrimonio'),
            ('Factor General (%)', 'general')
        ]

        for i, (label, key) in enumerate(fields):
            row = ctk.CTkFrame(form, fg_color='transparent')
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=label, width=220, anchor='w').pack(side='left', padx=(0,6))
            ent = ctk.CTkEntry(row, width=120)
            ent.pack(side='left')
            self.pct_entries[key] = ent

        btn_row = ctk.CTkFrame(parent, fg_color='transparent')
        btn_row.pack(fill='x', padx=8, pady=6)
        ctk.CTkButton(btn_row, text='Generar Proforma', command=self.apply_proforma, fg_color='#06B6D4').pack(side='left')

        # Result area
        self.proforma_result = ctk.CTkScrollableFrame(parent)
        self.proforma_result.pack(fill='both', expand=True, padx=8, pady=6)

        # If already have proforma in analyzer, show default
        # (No automatic generation yet)

    def apply_proforma(self):
        # Read percentage inputs
        pct_map = {}
        for key, ent in self.pct_entries.items():
            v = ent.get().strip()
            if v == '':
                continue
            try:
                pct_map[key] = float(v)
            except Exception:
                pct_map[key] = 0.0

        res = self.analyzer.generate_proforma(pct_map)

        # Clear result area
        for w in self.proforma_result.winfo_children():
            w.destroy()

        # Show Balance Proforma
        ctk.CTkLabel(self.proforma_result, text='Balance Proforma (monto y %)', font=ctk.CTkFont(weight='bold'), text_color='#111827').pack(anchor='w', pady=(6,4))
        self.render_table(self.proforma_result, res.get('vertical_bs'))

        # Show Estado Resultados Proforma
        ctk.CTkLabel(self.proforma_result, text='Estado de Resultados Proforma (monto y %)', font=ctk.CTkFont(weight='bold'), text_color='#111827').pack(anchor='w', pady=(8,4))
        self.render_table(self.proforma_result, res.get('vertical_is'))

    def render_ratios(self, parent):
        for w in parent.winfo_children():
            w.destroy()

        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.pack(fill='x', padx=8, pady=6)
        ctk.CTkLabel(top, text="Razones Financieras", font=ctk.CTkFont(size=16, weight='bold'), text_color="#111827").pack(side='left')

        # DuPont option
        options = ['DuPont (3 pasos)', 'DuPont (5 pasos)']
        self.dupont_sel = ctk.StringVar(value=options[0])
        opt = ctk.CTkOptionMenu(top, values=options, variable=self.dupont_sel, width=180)
        opt.pack(side='right')

        body = ctk.CTkScrollableFrame(parent)
        body.pack(fill='both', expand=True, padx=8, pady=6)

        ratios = self.analyzer.analysis_results.get('ratios', []) or []
        # Render ratios as a two-column list
        for r in ratios:
            nombre = r.get('nombre', '')
            valor = r.get('valor', None)
            ideal = r.get('ideal', '')
            if isinstance(valor, float):
                # Show percentages for ratio names that suggest percent
                if 'Margen' in nombre or 'RO' in nombre or 'DuPont' in nombre:
                    valor_s = f"{valor:.4f}"
                    # If it looks like a ratio between 0 and 1, show percent too
                    if 0 < valor <= 1:
                        valor_s = f"{valor:.2%}"
                else:
                    valor_s = f"{valor:,.2f}"
            else:
                valor_s = str(valor)

            frame = ctk.CTkFrame(body, fg_color="#FAFAFA")
            frame.pack(fill='x', pady=6, padx=4)
            ctk.CTkLabel(frame, text=f"{nombre}", text_color="#111827", font=ctk.CTkFont(weight='bold')).pack(side='left', padx=8, pady=6)
            ctk.CTkLabel(frame, text=f"Valor: {valor_s}", text_color="#374151").pack(side='right', padx=8)
            ctk.CTkLabel(frame, text=f"Ideal: {ideal}", text_color="#6B7280").pack(side='right')

