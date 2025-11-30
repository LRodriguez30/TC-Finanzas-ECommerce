import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import os
from backend.logic.financial_models import FinancialAnalyzer
from backend.logic.excel_handler import ExcelHandler
from .chatbot import ChatbotWindow
from ..theme_manager import get_color
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
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827")
        title.pack(side="left")
        
        # Contenedor de botones
        # Botones para descargar plantillas, importar años y exportar reportes
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Descargar Plantillas", command=self.download_templates, fg_color=get_color('card_bg'), text_color=get_color('text')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Importar Año Base", command=lambda: self.import_data('base'), fg_color=get_color('primary')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Importar Año Actual", command=lambda: self.import_data('current'), fg_color=get_color('primary')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color=get_color('success')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Chatbot", command=self.open_chatbot, fg_color=get_color('accent')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Interpretar", command=self.show_interpretations, fg_color=get_color('accent')).pack(side="left", padx=6)

        # --- Pestañas ---
        # Secciones del análisis financiero: Balance, Estado de Resultados, Fuentes/Usos, Razones y Gráficos
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
        
        # Estado inicial vacío
        # Muestra mensajes indicando que el usuario debe importar datos para ver resultados
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

        # Trigger analysis when both base and current are available
        if self.analyzer.base_bs is not None and self.analyzer.current_bs is not None and self.analyzer.base_is is not None and self.analyzer.current_is is not None:
            self.analyzer.perform_analysis()
            self.refresh_ui()

    def refresh_ui(self):
        # Limpia el contenido anterior de cada pestaña antes de renderizar los nuevos resultados
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

    def on_theme_change(self):
        # Called when palette changes — refresh UI elements if needed
        self.refresh_ui()

    def render_simple_table(self, parent, df):
        if df is None or df.empty: return
        for r, row in df.iterrows():
            ctk.CTkLabel(parent, text=f"{row['Cuenta']}: ${row['Monto']:.2f}", text_color="#374151").pack(anchor="w", pady=2)

    def render_charts(self, parent):
        # Gráfico de ejemplo: Total de Activos Año Base vs Año Actual
        # Compara la suma de activos entre ambos años para una vista rápida de cambios
        if self.analyzer.base_bs is None: return
        
        fig, ax = plt.subplots(figsize=(5, 4))
        # Suma de la columna 'Monto' para las cuentas clasificadas como 'Activo'
        base_assets = self.analyzer.base_bs[self.analyzer.base_bs['Tipo'] == 'Activo']['Monto'].sum()
        curr_assets = self.analyzer.current_bs[self.analyzer.current_bs['Tipo'] == 'Activo']['Monto'].sum()
        ax.bar(['Año Base', 'Año Actual'], [base_assets, curr_assets], color=['#E5E7EB', '#06B6D4'])
        ax.set_title("Total Activos", color="#111827")
        
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
        # Save comprehensive analysis to exports/latest_financial_report.xlsx
        out_dir = os.path.join(os.getcwd(), 'exports')
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'latest_financial_report.xlsx')

        # Prepare proforma pct_map from current entries (if any)
        pct_map = {}
        if hasattr(self, 'pct_entries') and isinstance(self.pct_entries, dict):
            for k, ent in self.pct_entries.items():
                try:
                    v = ent.get().strip()
                    if v != '':
                        pct_map[k] = float(v)
                except Exception:
                    continue

        proforma = self.analyzer.generate_proforma(pct_map) if (self.analyzer.current_bs is not None and self.analyzer.current_is is not None) else None

        with pd.ExcelWriter(out_path, engine='xlsxwriter') as writer:
            # Raw sheets
            if self.analyzer.base_bs is not None:
                self.analyzer.base_bs.to_excel(writer, sheet_name='Balance_Base_Raw', index=False)
            if self.analyzer.current_bs is not None:
                self.analyzer.current_bs.to_excel(writer, sheet_name='Balance_Actual_Raw', index=False)
            if self.analyzer.base_is is not None:
                self.analyzer.base_is.to_excel(writer, sheet_name='IS_Base_Raw', index=False)
            if self.analyzer.current_is is not None:
                self.analyzer.current_is.to_excel(writer, sheet_name='IS_Actual_Raw', index=False)

            # Analyses (vertical/horizontal)
            v = self.analyzer.analysis_results.get('vertical_bs_base')
            if v is not None and not v.empty:
                v.to_excel(writer, sheet_name='Vertical_BS_Base', index=False)
            v = self.analyzer.analysis_results.get('vertical_bs_actual')
            if v is not None and not v.empty:
                v.to_excel(writer, sheet_name='Vertical_BS_Actual', index=False)
            h = self.analyzer.analysis_results.get('horizontal_bs')
            if h is not None and not h.empty:
                h.to_excel(writer, sheet_name='Horizontal_BS', index=False)

            v = self.analyzer.analysis_results.get('vertical_is_base')
            if v is not None and not v.empty:
                v.to_excel(writer, sheet_name='Vertical_IS_Base', index=False)
            v = self.analyzer.analysis_results.get('vertical_is_actual')
            if v is not None and not v.empty:
                v.to_excel(writer, sheet_name='Vertical_IS_Actual', index=False)
            h = self.analyzer.analysis_results.get('horizontal_is')
            if h is not None and not h.empty:
                h.to_excel(writer, sheet_name='Horizontal_IS', index=False)

            # Ratios
            ratios = self.analyzer.analysis_results.get('ratios', []) or []
            if ratios:
                try:
                    df_ratios = pd.DataFrame(ratios)
                    df_ratios.to_excel(writer, sheet_name='Razones', index=False)
                except Exception:
                    # fallback: write as single-column text
                    pd.DataFrame({'Razones': [str(r) for r in ratios]}).to_excel(writer, sheet_name='Razones', index=False)

            # Fuentes y Usos
            su = self.analyzer.analysis_results.get('sources_uses', {}) or {}
            if isinstance(su, dict):
                if 'Fuentes' in su and su['Fuentes'] is not None and not su['Fuentes'].empty:
                    su['Fuentes'].to_excel(writer, sheet_name='Fuentes', index=False)
                if 'Usos' in su and su['Usos'] is not None and not su['Usos'].empty:
                    su['Usos'].to_excel(writer, sheet_name='Usos', index=False)

            # Proforma (if generated)
            if proforma:
                if proforma.get('bs') is not None and not proforma['bs'].empty:
                    proforma['bs'].to_excel(writer, sheet_name='Proforma_BS', index=False)
                if proforma.get('is') is not None and not proforma['is'].empty:
                    proforma['is'].to_excel(writer, sheet_name='Proforma_IS', index=False)
                if proforma.get('vertical_bs') is not None and not proforma['vertical_bs'].empty:
                    proforma['vertical_bs'].to_excel(writer, sheet_name='Proforma_Vert_BS', index=False)
                if proforma.get('vertical_is') is not None and not proforma['vertical_is'].empty:
                    proforma['vertical_is'].to_excel(writer, sheet_name='Proforma_Vert_IS', index=False)

            # Interpretations / recommendations
            try:
                interp_lines = []
                # reuse show_interpretations logic but without UI
                ratios_local = self.analyzer.analysis_results.get('ratios', []) or []
                if not ratios_local:
                    interp_lines.append('No hay datos suficientes para generar interpretaciones.')
                else:
                    liq = next((r for r in ratios_local if 'Liquidez Corriente' in r.get('nombre','')), None)
                    if liq and liq.get('valor') is not None:
                        if liq['valor'] < 1:
                            interp_lines.append('La liquidez corriente es baja (<1): riesgo de falta de recursos para obligaciones de corto plazo.')
                        elif liq['valor'] < 1.5:
                            interp_lines.append('La liquidez es moderada; conviene vigilar el capital de trabajo.')
                        else:
                            interp_lines.append('La liquidez parece adecuada.')

                    margen = next((r for r in ratios_local if 'Margen de Utilidad Neta' in r.get('nombre','')), None)
                    if margen and margen.get('valor') is not None:
                        if margen['valor'] < 0.05:
                            interp_lines.append('Margen Neto bajo: revisar estructura de costos y precios.')
                        else:
                            interp_lines.append('Margen Neto aceptable.')

                    indebt = next((r for r in ratios_local if 'Índice de Endeudamiento' in r.get('nombre','')), None)
                    if indebt and indebt.get('valor') is not None:
                        if indebt['valor'] > 0.6:
                            interp_lines.append('Alto apalancamiento: considerar reducir deuda o aumentar patrimonio.')
                        else:
                            interp_lines.append('Nivel de endeudamiento moderado.')

                    interp_lines.append('Recomendaciones generales:')
                    interp_lines.append('- Mejorar rotación de activos si las ventas son bajas respecto a activos.')
                    interp_lines.append('- Revisar inventarios y cuentas por cobrar para liberar capital de trabajo.')

                pd.DataFrame({'Interpretaciones': interp_lines}).to_excel(writer, sheet_name='Interpretaciones', index=False)
            except Exception:
                pass

        print(f"Reporte guardado en {out_path}")

    def open_chatbot(self):
        ChatbotWindow(self.master)

    def show_interpretations(self):
        # Generate simple textual interpretations based on ratios and trends
        text = []
        ratios = self.analyzer.analysis_results.get('ratios', []) or []
        if not ratios:
            text.append('No hay datos suficientes para generar interpretaciones.')
        else:
            # Liquidity
            liq = next((r for r in ratios if 'Liquidez Corriente' in r.get('nombre','')), None)
            if liq and liq.get('valor') is not None:
                if liq['valor'] < 1:
                    text.append('La liquidez corriente es baja (<1): riesgo de falta de recursos para obligaciones de corto plazo.')
                elif liq['valor'] < 1.5:
                    text.append('La liquidez es moderada; conviene vigilar el capital de trabajo.')
                else:
                    text.append('La liquidez parece adecuada.')

            # Profitability
            margen = next((r for r in ratios if 'Margen de Utilidad Neta' in r.get('nombre','')), None)
            if margen and margen.get('valor') is not None:
                if margen['valor'] < 0.05:
                    text.append('Margen Neto bajo: revisar estructura de costos y precios.')
                else:
                    text.append('Margen Neto aceptable.')

            # Leverage
            indebt = next((r for r in ratios if 'Índice de Endeudamiento' in r.get('nombre','')), None)
            if indebt and indebt.get('valor') is not None:
                if indebt['valor'] > 0.6:
                    text.append('Alto apalancamiento: considerar reducir deuda o aumentar patrimonio.')
                else:
                    text.append('Nivel de endeudamiento moderado.')

            text.append('\nRecomendaciones generales:')
            text.append('- Mejorar rotación de activos si las ventas son bajas respecto a activos.')
            text.append('- Revisar inventarios y cuentas por cobrar para liberar capital de trabajo.')

        # Show in a popup
        popup = ctk.CTkToplevel(self)
        popup.geometry('600x400')
        popup.title('Interpretaciones y Recomendaciones')
        body = ctk.CTkScrollableFrame(popup)
        body.pack(fill='both', expand=True, padx=8, pady=8)
        for p in text:
            ctk.CTkLabel(body, text=p, wraplength=560, text_color=get_color('text')).pack(anchor='w', pady=6)

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

