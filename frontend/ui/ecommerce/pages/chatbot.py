import customtkinter as ctk
from backend.logic.excel_handler import ExcelHandler
from backend.logic.financial_models import FinancialAnalyzer
import os
import requests
import json
import threading

# Para pruebas locales puedes pegar aquí tu API Key temporalmente.
# ADVERTENCIA: guardar claves en el código fuente es inseguro. Reemplaza
# el valor por tu API Key solo para pruebas y luego usa variables de entorno.
API_KEY = 'AIzaSyCqPH96SHeLx9GpChQ37SASfQP42yJAVKI'  # <-- Pega tu API Key aquí manualmente para probar localmente


class ChatbotWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Chatbot Financiero')
        self.geometry('700x500')

        # no bearer token support (use API key via environment variable)

        self.chat_area = ctk.CTkScrollableFrame(self)
        self.chat_area.pack(fill='both', expand=True, padx=8, pady=8)

        self.entry = ctk.CTkEntry(self, placeholder_text='Escribe aquí...')
        self.entry.pack(fill='x', padx=8, pady=(0,8))
        self.entry.bind('<Return>', self.on_enter)

        # On open, try to load latest exported report automatically (in background)
        t = threading.Thread(target=self.auto_analyze, daemon=True)
        t.start()

    def post_message(self, sender, text):
        frame = ctk.CTkFrame(self.chat_area, fg_color='transparent')
        frame.pack(fill='x', pady=6)
        ctk.CTkLabel(frame, text=f"{sender}:", text_color='#6B7280').pack(anchor='w')
        ctk.CTkLabel(frame, text=text, wraplength=650).pack(anchor='w', pady=2)

    def safe_post_message(self, sender, text):
        # Schedule UI update on main thread only if widget still exists
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        def _post():
            try:
                if not self.winfo_exists():
                    return
                self.post_message(sender, text)
            except Exception:
                # Silently ignore UI errors if window destroyed
                return

        try:
            self.after(0, _post)
        except Exception:
            # If after fails because tk is destroyed, ignore
            return

    def on_enter(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        # Post synchronously the user message to UI (safe)
        try:
            self.safe_post_message('Usuario', msg)
        except Exception:
            pass
        # (no token commands supported)
        # Simple rule: if user asks for 'resumen' or 'recomend', show last analysis
        if 'resumen' in msg.lower() or 'recomend' in msg.lower() or 'analiz' in msg.lower():
            t = threading.Thread(target=self.auto_analyze, daemon=True)
            t.start()
        else:
            self.safe_post_message('Bot', 'Actualmente el chatbot responde con el análisis automático del último reporte exportado. Escribe "resumen" para obtenerlo.')
        self.entry.delete(0, 'end')

    def auto_analyze(self):
        out_dir = os.path.join(os.getcwd(), 'exports')
        out_path = os.path.join(out_dir, 'latest_financial_report.xlsx')
        if not os.path.exists(out_path):
            self.safe_post_message('Bot', 'No se encontró un reporte exportado. Usa la opción "Exportar Reporte" en Análisis Financiero para generar `exports/latest_financial_report.xlsx`.')
            return

        excel = ExcelHandler()
        try:
            bs_base = None
            bs_actual = None
            is_base = None
            is_actual = None
            # ExcelHandler.load_financial_data espera hojas 'Balance General' y 'Estado Resultados',
            # pero en export usamos nombres diferentes; leer manualmente con pandas
            import pandas as pd
            xls = pd.ExcelFile(out_path)

            # Helper to find sheet by exact candidates or by keywords
            def find_sheet(candidates=None, keywords=None):
                candidates = candidates or []
                for c in candidates:
                    if c in xls.sheet_names:
                        return c
                if keywords:
                    for s in xls.sheet_names:
                        name = s.lower()
                        if all(k.lower() in name for k in keywords):
                            return s
                return None

            # Helper to normalize dataframe columns to expected names
            def normalize_df(df):
                if df is None:
                    return None
                # standardize column names: remove surrounding spaces
                cols = {c: c.strip() for c in df.columns}
                df = df.rename(columns=cols)

                mapping = {}
                lower_cols = {c.lower(): c for c in df.columns}
                # Cuenta
                for candidate in ['cuenta', 'account', 'name']:
                    if candidate in lower_cols:
                        mapping[lower_cols[candidate]] = 'Cuenta'
                        break
                # Tipo
                for candidate in ['tipo', 'type']:
                    if candidate in lower_cols:
                        mapping[lower_cols[candidate]] = 'Tipo'
                        break
                # Monto
                for candidate in ['monto', 'amount', 'valor', 'balance']:
                    if candidate in lower_cols:
                        mapping[lower_cols[candidate]] = 'Monto'
                        break

                if mapping:
                    df = df.rename(columns=mapping)

                # Ensure Monto is numeric
                if 'Monto' in df.columns:
                    try:
                        df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0.0)
                    except Exception:
                        pass

                return df

            # Candidates include the names used by export_report plus common variants
            bs_base_sheet = find_sheet(candidates=['Balance_Base_Raw', 'Balance_Base', 'Balance Base', 'Balance_Base_Raw', 'Balance_Base_Raw']) or find_sheet(keywords=['balance', 'base'])
            bs_actual_sheet = find_sheet(candidates=['Balance_Actual_Raw', 'Balance_Actual', 'Balance Actual', 'Balance_Actual_Raw']) or find_sheet(keywords=['balance', 'actual'])
            is_base_sheet = find_sheet(candidates=['IS_Base_Raw', 'IS_Base', 'IS Base', 'IS_Base_Raw', 'Estado_Resultados', 'Estado Resultados', 'Estado Resultados Base']) or find_sheet(keywords=['estado', 'base', 'result'])
            is_actual_sheet = find_sheet(candidates=['IS_Actual_Raw', 'IS_Actual', 'IS Actual', 'IS_Actual_Raw', 'Estado_Resultados', 'Estado Resultados', 'Estado Resultados Actual']) or find_sheet(keywords=['estado', 'actual', 'result'])

            if bs_base_sheet:
                try:
                    bs_base = normalize_df(pd.read_excel(xls, sheet_name=bs_base_sheet))
                except Exception:
                    bs_base = None
            if bs_actual_sheet:
                try:
                    bs_actual = normalize_df(pd.read_excel(xls, sheet_name=bs_actual_sheet))
                except Exception:
                    bs_actual = None
            if is_base_sheet:
                try:
                    is_base = normalize_df(pd.read_excel(xls, sheet_name=is_base_sheet))
                except Exception:
                    is_base = None
            if is_actual_sheet:
                try:
                    is_actual = normalize_df(pd.read_excel(xls, sheet_name=is_actual_sheet))
                except Exception:
                    is_actual = None

            # Last-resort: try the ExcelHandler loader which expects 'Balance General' and 'Estado Resultados'
            if (bs_base is None and bs_actual is None) and (is_base is None and is_actual is None):
                try:
                    bs_tmp, is_tmp = ExcelHandler.load_financial_data(out_path)
                    # If load_financial_data returned a tuple with both sheets, use them as 'actual'
                    if bs_tmp is not None and is_tmp is not None:
                        # normalize and set as actual if nothing else found
                        try:
                            bs_tmp = normalize_df(bs_tmp)
                        except Exception:
                            pass
                        try:
                            is_tmp = normalize_df(is_tmp)
                        except Exception:
                            pass
                        if bs_actual is None:
                            bs_actual = bs_tmp
                        if is_actual is None:
                            is_actual = is_tmp
                except Exception:
                    pass

            analyzer = FinancialAnalyzer()
            try:
                analyzer.load_data(bs_base, bs_actual, is_base, is_actual)
            except Exception as e:
                self.safe_post_message('Bot', f'Error al procesar datos: {e}')
                return

            # Build a structured prompt for Gemini containing ratios and small data samples.
            ratios = analyzer.analysis_results.get('ratios', []) or []
            # If there are no ratios, abort early
            if not ratios:
                self.safe_post_message('Bot', 'No se encontraron razones calculadas en los datos. Verifica las hojas y columnas del reporte.')
                return

            # Prepare ratios text
            ratios_lines = []
            for r in ratios:
                nombre = r.get('nombre', 'N/A')
                val = r.get('valor', None)
                ideal = r.get('ideal', '')
                try:
                    if isinstance(val, (int, float)) and val is not None:
                        # For ratios that are proportions, show percent when likely
                        if abs(val) <= 10 and any(k in nombre.lower() for k in ['margen', 'roe', 'roa', 'rotación', 'rotacion']):
                            val_str = f"{val:.4f}"
                        else:
                            val_str = f"{val}"
                    else:
                        val_str = str(val)
                except Exception:
                    val_str = str(val)
                ratios_lines.append(f"{nombre}: {val_str} {'('+ideal+')' if ideal else ''}")

            # Small samples of vertical analyses (if available)
            vert_is = analyzer.analysis_results.get('vertical_is_actual')
            vert_bs = analyzer.analysis_results.get('vertical_bs_actual')
            def df_preview(df, max_rows=8):
                if df is None or df.empty:
                    return ''
                try:
                    # show Cuenta and Monto and Vertical % if present
                    cols = []
                    for c in ['Cuenta', 'Monto', 'Vertical %']:
                        if c in df.columns:
                            cols.append(c)
                    preview = df[cols].head(max_rows).to_csv(index=False, sep=';')
                    return preview
                except Exception:
                    return ''

            prompt_parts = [
                'Eres un experto contable y financiero. A partir de los siguientes datos, entrega un análisis claro (3-5 párrafos) y 6 recomendaciones accionables y priorizadas para la empresa. Usa lenguaje en español.' ,
                '\n-- Razones financieras (nombre: valor (ideal)) --\n',
                '\n'.join(ratios_lines),
                '\n-- Muestra breve del Estado de Resultados (Año Actual) --\n',
                df_preview(vert_is),
                '\n-- Muestra breve del Balance (Año Actual) --\n',
                df_preview(vert_bs),
                '\nFin del reporte. Responde sólo con el análisis y las recomendaciones, sin pasos técnicos para el software.'
            ]
            prompt = '\n'.join([p for p in prompt_parts if p])

            # Prefer API_KEY constant in file for quick tests, otherwise check env var
            api_key = API_KEY or os.environ.get('GEMINI_API_KEY') or os.environ.get('GEN_API_KEY')
            if not api_key:
                self.safe_post_message('Bot', 'No hay API Key configurada. Pega tu API Key en la constante `API_KEY` dentro de este archivo o define `GEMINI_API_KEY` en el entorno.')
                return

            # Inform user that Gemini is being queried
            self.safe_post_message('Bot', 'Consultando Gemini para generar las interpretaciones y recomendaciones...')
            try:
                gem_response = self.call_gemini(prompt, api_key)
                # Show Gemini response or error
                self.safe_post_message('Bot (Gemini)', gem_response)
            except Exception as e:
                self.safe_post_message('Bot', f'Error al solicitar Gemini: {e}')
        except Exception as e:
            self.safe_post_message('Bot', f'Error al analizar el archivo: {e}')

    def call_gemini(self, prompt: str, api_key: str = None) -> str:
        """Usa la librería oficial `google.generativeai` si está instalada.

        Intenta instanciar varios modelos comunes y devuelve la primera respuesta válida.
        """
        try:
            import google.generativeai as genai
        except Exception:
            return 'Error: el paquete `google-generativeai` no parece estar instalado en el entorno. Ejecuta `pip install google-generativeai`.'

        if not api_key:
            return 'No API Key proporcionada para Gemini.'

        try:
            # Configure client (usa GEMINI_API_KEY si api_key es None)
            genai.configure(api_key=api_key)
        except Exception as e:
            return f'Error configurando el cliente generativeai: {e}'

        # Model candidates ordenados por preferencia
        model_candidates = [
            'models/gemini-pro-latest',
            'models/gemini-flash-latest',
            'models/gemini-2.5-flash',
            'models/gemini-2.5-pro',
            'models/gemini-2.0-flash',
            'models/text-bison-001',
        ]

        last_exc = None
        for m in model_candidates:
            try:
                model = genai.GenerativeModel(model_name=m)
                # generate_content espera una lista de Contents; cada Content tiene 'parts'
                resp = model.generate_content([{'parts': [{'text': prompt}]}])

                # Intentar extraer texto de la respuesta de forma segura
                text = None
                try:
                    if hasattr(resp, 'text') and resp.text:
                        text = resp.text
                    elif hasattr(resp, 'candidates'):
                        cand = getattr(resp, 'candidates')
                        if cand:
                            first = cand[0]
                            # Algunos candidatos tienen 'content' o 'parts'
                            if hasattr(first, 'content'):
                                parts = getattr(first, 'content')
                                # parts puede ser iterable de objetos con 'text'
                                out = []
                                for p in parts:
                                    if hasattr(p, 'text'):
                                        out.append(getattr(p, 'text') or '')
                                    else:
                                        out.append(str(p))
                                text = '\n'.join(out)
                            else:
                                text = str(first)
                    elif hasattr(resp, 'output'):
                        text = str(resp.output)
                except Exception:
                    text = None

                if text:
                    return text
                # Fallback: devolver representación completa
                return str(resp)
            except Exception as e:
                last_exc = e
                # probar siguiente modelo
                continue

        # Si ninguno funcionó, devolver el último error con guía
        if last_exc is not None:
            return f'No se obtuvo respuesta de los modelos probados. Último error: {last_exc}'
        return 'No fue posible comunicarse con Gemini.'
