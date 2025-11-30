import pandas as pd

class FinancialAnalyzer:
    """Analizador financiero simple pero funcional.

    Provee:
    - Análisis vertical (con porcentajes) para Balance e Informe de Resultado
    - Análisis horizontal (variación $ y %)
    - Cálculo de múltiples razones financieras (nombres en español)
    - DuPont 3 pasos y DuPont extendido (5 pasos)
    - Fuentes y usos simplificados
    """

    def __init__(self):
        self.base_bs = None  # Balance Sheet Año Base (DataFrame)
        self.current_bs = None  # Balance Sheet Año Actual (DataFrame)
        self.base_is = None  # Income Statement Año Base
        self.current_is = None  # Income Statement Año Actual

        self.analysis_results = {}

    def load_data(self, base_bs_df, current_bs_df, base_is_df, current_is_df):
        self.base_bs = base_bs_df
        self.current_bs = current_bs_df
        self.base_is = base_is_df
        self.current_is = current_is_df
        self.perform_analysis()

    def perform_analysis(self):
        # Vertical: both año base y año actual
        self.analysis_results['vertical_bs_base'] = self._vertical_analysis(self.base_bs, kind='bs')
        self.analysis_results['vertical_bs_actual'] = self._vertical_analysis(self.current_bs, kind='bs')
        self.analysis_results['horizontal_bs'] = self._horizontal_analysis(self.base_bs, self.current_bs)
        self.analysis_results['vertical_is_base'] = self._vertical_analysis(self.base_is, kind='is')
        self.analysis_results['vertical_is_actual'] = self._vertical_analysis(self.current_is, kind='is')
        self.analysis_results['horizontal_is'] = self._horizontal_analysis(self.base_is, self.current_is)
        self.analysis_results['ratios'] = self._calculate_ratios()
        self.analysis_results['sources_uses'] = self._calculate_sources_uses()

    def generate_proforma(self, pct_map=None):
        """Genera una proforma simple aplicando porcentajes a las cuentas del año actual.

        pct_map: diccionario con claves opcionales:
          - 'ventas', 'inventarios', 'cxc', 'activos_fijos', 'pasivos', 'patrimonio', 'general'
        Los valores se esperan en porcentaje (p.ej. 10 para +10%).
        """
        if self.current_bs is None or self.current_is is None:
            return {'bs': pd.DataFrame(), 'is': pd.DataFrame(), 'vertical_bs': pd.DataFrame(), 'vertical_is': pd.DataFrame()}

        pct_map = pct_map or {}
        def pct_to_factor(key):
            v = pct_map.get(key, None)
            if v is None:
                return None
            try:
                return 1.0 + float(v) / 100.0
            except Exception:
                return None

        f_ventas = pct_to_factor('ventas') or pct_to_factor('general') or 1.0
        f_inventarios = pct_to_factor('inventarios') or pct_to_factor('general') or 1.0
        f_cxc = pct_to_factor('cxc') or pct_to_factor('general') or 1.0
        f_activos_fijos = pct_to_factor('activos_fijos') or pct_to_factor('general') or 1.0
        f_pasivos = pct_to_factor('pasivos') or pct_to_factor('general') or 1.0
        f_patrimonio = pct_to_factor('patrimonio') or pct_to_factor('general') or 1.0

        # Proyectar estado de resultados: aplicar factor a ventas y a otras cuentas proporcionalmente
        is_proj = self.current_is.copy()
        for idx, row in is_proj.iterrows():
            cuenta = row.get('Cuenta', '')
            monto = float(row.get('Monto', 0) or 0)
            if 'Ventas' in cuenta:
                is_proj.at[idx, 'Monto'] = monto * f_ventas
            else:
                # aplicar factor general
                is_proj.at[idx, 'Monto'] = monto * (pct_to_factor('general') or 1.0)

        # Proyectar balance: aplicar factores según cuentas claves
        bs_proj = self.current_bs.copy()
        for idx, row in bs_proj.iterrows():
            cuenta = row.get('Cuenta', '')
            monto = float(row.get('Monto', 0) or 0)
            tipo = row.get('Tipo', '')
            if 'Inventario' in cuenta or 'Inventarios' in cuenta:
                bs_proj.at[idx, 'Monto'] = monto * f_inventarios
            elif 'Cuentas por Cobrar' in cuenta or 'Cuentas por Cobran' in cuenta or 'Cobrar' in cuenta:
                bs_proj.at[idx, 'Monto'] = monto * f_cxc
            elif 'Activo' in tipo and ('Fijo' in cuenta or 'Activos Fijos' in cuenta):
                bs_proj.at[idx, 'Monto'] = monto * f_activos_fijos
            elif tipo == 'Pasivo':
                bs_proj.at[idx, 'Monto'] = monto * f_pasivos
            elif tipo == 'Patrimonio':
                bs_proj.at[idx, 'Monto'] = monto * f_patrimonio
            else:
                # default
                bs_proj.at[idx, 'Monto'] = monto * (pct_to_factor('general') or 1.0)

        vertical_bs_proj = self._vertical_analysis(bs_proj, kind='bs')
        vertical_is_proj = self._vertical_analysis(is_proj, kind='is')

        return {'bs': bs_proj, 'is': is_proj, 'vertical_bs': vertical_bs_proj, 'vertical_is': vertical_is_proj}

    def _vertical_analysis(self, df, kind='is'):
        """Calcula porcentaje vertical para cada fila.

        kind: 'bs' para Balance (usa total activos), 'is' para Estado de Resultado (usa ventas netas)
        """
        if df is None or df.empty:
            return pd.DataFrame()

        result = df.copy()

        # Determinar total apropiado
        total = None
        if kind == 'bs':
            if 'Tipo' in result.columns and 'Activo' in result['Tipo'].values:
                total = float(result.loc[result['Tipo'] == 'Activo', 'Monto'].sum())
        else:  # is
            if 'Cuenta' in result.columns and 'Ventas Netas' in result['Cuenta'].values:
                total = float(result.loc[result['Cuenta'] == 'Ventas Netas', 'Monto'].sum())

        if total is None or total == 0:
            # Fallback: suma absoluta para que los porcentajes sean representativos
            total = float(result['Monto'].abs().sum()) if 'Monto' in result.columns else 1.0

        result['Vertical %'] = (result['Monto'] / total) * 100
        return result

    def _horizontal_analysis(self, base_df, current_df):
        if base_df is None or current_df is None:
            return pd.DataFrame()

        merged = pd.merge(base_df, current_df, on="Cuenta", how='outer', suffixes=('_Base', '_Actual'))
        # Ensure Monto columns exist
        if 'Monto_Base' not in merged.columns and 'Monto_Base' in merged.columns:
            pass
        # Fill NaN with 0
        for col in merged.columns:
            if merged[col].dtype == object:
                continue
        merged['Monto Base'] = merged.get('Monto_Base', merged.get('Monto_Base', merged.get('Monto_Base', 0)))
        merged['Monto Actual'] = merged.get('Monto_Actual', merged.get('Monto_Actual', merged.get('Monto_Actual', 0)))

        # Prefer original names if present
        if 'Monto_Base' in merged.columns:
            merged['Monto Base'] = merged['Monto_Base']
        if 'Monto_Actual' in merged.columns:
            merged['Monto Actual'] = merged['Monto_Actual']

        merged['Monto Base'] = merged['Monto Base'].fillna(0).astype(float)
        merged['Monto Actual'] = merged['Monto Actual'].fillna(0).astype(float)

        merged['Variación $'] = merged['Monto Actual'] - merged['Monto Base']
        merged['Variación %'] = merged.apply(lambda r: (r['Variación $'] / r['Monto Base'] * 100) if r['Monto Base'] != 0 else None, axis=1)

        # Keep common order
        cols = ['Cuenta', 'Monto Base', 'Monto Actual', 'Variación $', 'Variación %']
        for c in cols:
            if c not in merged.columns:
                merged[c] = None

        return merged[cols]

    def _calculate_ratios(self):
        """Calcula un conjunto de razones financieras con nombres en español."""
        if self.current_bs is None or self.current_is is None:
            return []

        bs = self.current_bs
        isf = self.current_is

        def get_account(df, name):
            try:
                return float(df.loc[df['Cuenta'] == name, 'Monto'].sum())
            except Exception:
                return 0.0

        activos = float(bs.loc[bs['Tipo'] == 'Activo', 'Monto'].sum()) if 'Tipo' in bs.columns else float(bs['Monto'].sum())
        pasivos = float(bs.loc[bs['Tipo'] == 'Pasivo', 'Monto'].sum()) if 'Tipo' in bs.columns else 0.0
        patrimonio = float(bs.loc[bs['Tipo'] == 'Patrimonio', 'Monto'].sum()) if 'Tipo' in bs.columns else max(activos - pasivos, 0.0)

        ventas = get_account(isf, 'Ventas Netas')
        costo_ventas = get_account(isf, 'Costo de Ventas')
        gastos_oper = get_account(isf, 'Gastos Operativos')
        gastos_fin = get_account(isf, 'Gastos Financieros')
        impuestos = get_account(isf, 'Impuestos')

        utilidad_neta = ventas - costo_ventas - gastos_oper - gastos_fin - impuestos
        ebit = ventas - costo_ventas - gastos_oper
        ebt = ebit - gastos_fin

        def safe_div(a, b):
            try:
                return a / b if b not in (0, None) else None
            except Exception:
                return None

        ratios = []
        ratios.append({'nombre': 'Liquidez Corriente', 'valor': safe_div(activos, pasivos), 'ideal': '> 1.0'})
        inventarios = get_account(bs, 'Inventarios')
        ratios.append({'nombre': 'Prueba Ácida', 'valor': safe_div((activos - inventarios), pasivos), 'ideal': '> 1.0'})
        ratios.append({'nombre': 'Capital de Trabajo', 'valor': activos - pasivos, 'ideal': 'Positivo'})
        ratios.append({'nombre': 'Rotación de Inventarios', 'valor': safe_div(costo_ventas, inventarios), 'ideal': 'Alta'})
        cxc = get_account(bs, 'Cuentas por Cobrar')
        ratios.append({'nombre': 'Periodo Promedio de Cobro (días)', 'valor': (safe_div(cxc, ventas) * 365) if ventas else None, 'ideal': 'Bajo'})
        ratios.append({'nombre': 'Rotación de Activos Totales', 'valor': safe_div(ventas, activos), 'ideal': 'Alto'})
        ratios.append({'nombre': 'Índice de Endeudamiento (Pasivo/Activo)', 'valor': safe_div(pasivos, activos), 'ideal': '< 0.5'})
        ratios.append({'nombre': 'Margen de Utilidad Bruta', 'valor': safe_div((ventas - costo_ventas), ventas), 'ideal': 'Alto'})
        ratios.append({'nombre': 'Margen de Utilidad Operativa', 'valor': safe_div(ebit, ventas), 'ideal': 'Alto'})
        ratios.append({'nombre': 'Margen de Utilidad Neta', 'valor': safe_div(utilidad_neta, ventas), 'ideal': 'Alto'})
        ratios.append({'nombre': 'ROA (Rent. sobre Activos)', 'valor': safe_div(utilidad_neta, activos), 'ideal': 'Alto'})
        ratios.append({'nombre': 'ROE (Rent. sobre Patrimonio)', 'valor': safe_div(utilidad_neta, patrimonio), 'ideal': 'Alto'})
        ratios.append({'nombre': 'Cobertura de Intereses (EBIT/Intereses)', 'valor': safe_div(ebit, gastos_fin), 'ideal': '> 1.5'})

        # DuPont 3 pasos
        margen_neto = safe_div(utilidad_neta, ventas)
        rot_activos = safe_div(ventas, activos)
        multiplicador_fin = safe_div(activos, patrimonio)
        dupont_3 = None
        if margen_neto is not None and rot_activos is not None and multiplicador_fin is not None:
            dupont_3 = margen_neto * rot_activos * multiplicador_fin

        ratios.append({'nombre': 'DuPont (3 pasos) - ROE', 'valor': dupont_3, 'ideal': 'Alto'})

        # DuPont extendido (5 pasos): Tax burden * Interest burden * Operating margin * Asset turnover * Equity multiplier
        tax_burden = safe_div(utilidad_neta, ebt) if ebt not in (0, None) else None
        interest_burden = safe_div(ebt, ebit) if ebit not in (0, None) else None
        operating_margin = safe_div(ebit, ventas)
        assets_turnover = rot_activos
        equity_multiplier = multiplicador_fin

        dupont_5 = None
        if (tax_burden is not None and interest_burden is not None and operating_margin is not None
                and assets_turnover is not None and equity_multiplier is not None):
            dupont_5 = tax_burden * interest_burden * operating_margin * assets_turnover * equity_multiplier

        ratios.append({'nombre': 'DuPont (5 pasos) - ROE Extendido', 'valor': dupont_5, 'ideal': 'Alto'})

        return ratios

    def _calculate_sources_uses(self):
        # Sources: Decrease in Asset, Increase in Liability/Equity
        # Uses: Increase in Asset, Decrease in Liability/Equity
        if self.base_bs is None or self.current_bs is None:
            return {'Fuentes': pd.DataFrame(), 'Usos': pd.DataFrame()}

        merged = pd.merge(self.base_bs, self.current_bs, on="Cuenta", how='outer', suffixes=('_Base', '_Actual'))
        # Normalize Monto columns
        merged['Monto_Base'] = merged.get('Monto_Base', merged.get('Monto_Base', 0)).fillna(0)
        merged['Monto_Actual'] = merged.get('Monto_Actual', merged.get('Monto_Actual', 0)).fillna(0)
        # If named differently, try generic
        if 'Monto' in self.base_bs.columns and 'Monto' in self.current_bs.columns:
            merged['Monto_Base'] = merged.get('Monto_Base', merged.get('Monto', 0))
            merged['Monto_Actual'] = merged.get('Monto_Actual', merged.get('Monto', 0))

        merged['Diff'] = merged['Monto_Actual'] - merged['Monto_Base']

        sources = []
        uses = []

        for _, row in merged.iterrows():
            diff = row['Diff'] if not pd.isna(row['Diff']) else 0
            tipo = row.get('Tipo', None)

            # If tipo is unknown, use sign heuristics: increase in asset = use, decrease = source
            if tipo == 'Activo':
                if diff < 0:
                    sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff > 0:
                    uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
            else:
                # Pasivo/Patrimonio or unknown
                if diff > 0:
                    sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff < 0:
                    uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})

        return {'Fuentes': pd.DataFrame(sources), 'Usos': pd.DataFrame(uses)}

