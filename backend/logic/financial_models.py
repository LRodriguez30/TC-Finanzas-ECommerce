import pandas as pd

class FinancialAnalyzer:
    def __init__(self):
        self.base_bs = None # Balance Sheet (Año base) - DataFrame con cuentas y montos del año base
        self.current_bs = None # Balance Sheet (Año actual) - DataFrame con cuentas y montos del año actual
        self.base_is = None # Estado de Resultados (Año base) - DataFrame con cuentas y montos del año base
        self.current_is = None # Estado de Resultados (Año actual) - DataFrame con cuentas y montos del año actual
        
        self.analysis_results = {}

    def load_data(self, base_bs_df, current_bs_df, base_is_df, current_is_df):
        self.base_bs = base_bs_df
        self.current_bs = current_bs_df
        self.base_is = base_is_df
        self.current_is = current_is_df
        
        self.perform_analysis()

    def perform_analysis(self):
        self.analysis_results['vertical_bs'] = self._vertical_analysis(self.current_bs)
        self.analysis_results['horizontal_bs'] = self._horizontal_analysis(self.base_bs, self.current_bs)
        self.analysis_results['vertical_is'] = self._vertical_analysis(self.current_is)
        self.analysis_results['horizontal_is'] = self._horizontal_analysis(self.base_is, self.current_is)
        self.analysis_results['ratios'] = self._calculate_ratios()
        self.analysis_results['sources_uses'] = self._calculate_sources_uses()

    def _vertical_analysis(self, df):
        # Asume que existe la columna 'Monto'. Calcula el porcentaje sobre el total.
        # Para Balance (BS): % sobre Total Activos. Para Estado de Resultados (IS): % sobre Ventas Totales.
        if df is None or df.empty: return pd.DataFrame()
        
        result = df.copy()
        total = result['Monto'].max() # Simplificación: se asume que el valor máximo representa el total (Activos o Ventas)
        # En un caso real habría que buscar filas explícitas como 'TOTAL ACTIVOS' o 'VENTAS NETAS'
        
        result['Vertical %'] = (result['Monto'] / total) * 100
        return result

    def _horizontal_analysis(self, base_df, current_df):
        if base_df is None or current_df is None: return pd.DataFrame()
        
        # Fusiona por nombre de cuenta para comparar valores entre año base y año actual
        merged = pd.merge(base_df, current_df, on="Cuenta", suffixes=('_Base', '_Actual'))
        merged['Variación $'] = merged['Monto_Actual'] - merged['Monto_Base']
        merged['Variación %'] = (merged['Variación $'] / merged['Monto_Base']) * 100
        return merged

    def _calculate_ratios(self):
        # Calcula un conjunto de razones financieras basadas en los DataFrames
        # Espera que self.base_bs, self.current_bs, self.base_is, self.current_is existan
        if self.current_bs is None or self.current_is is None:
            return pd.DataFrame()

        def amt(df, cuenta_name):
            try:
                return float(df.loc[df['Cuenta'] == cuenta_name, 'Monto'].sum())
            except Exception:
                return 0.0

        def sum_tipo(df, tipo_name):
            try:
                return float(df.loc[df['Tipo'] == tipo_name, 'Monto'].sum())
            except Exception:
                return 0.0

        # Valores actuales
        ventas_curr = amt(self.current_is, 'Ventas Netas')
        cogs_curr = amt(self.current_is, 'Costo de Ventas')
        op_exp_curr = amt(self.current_is, 'Gastos Operativos')
        fin_exp_curr = amt(self.current_is, 'Gastos Financieros')
        impuestos_curr = amt(self.current_is, 'Impuestos')

        efectivo_curr = amt(self.current_bs, 'Efectivo')
        cxc_curr = amt(self.current_bs, 'Cuentas por Cobrar')
        inventarios_curr = amt(self.current_bs, 'Inventarios')
        activos_fijos_curr = amt(self.current_bs, 'Activos Fijos')
        pasivos_curr = sum_tipo(self.current_bs, 'Pasivo')
        patrimonio_curr = sum_tipo(self.current_bs, 'Patrimonio')
        activos_totales_curr = sum_tipo(self.current_bs, 'Activo')

        # Valores base (si existen)
        if self.base_bs is not None and self.base_is is not None:
            ventas_base = amt(self.base_is, 'Ventas Netas')
            cogs_base = amt(self.base_is, 'Costo de Ventas')
            op_exp_base = amt(self.base_is, 'Gastos Operativos')
            fin_exp_base = amt(self.base_is, 'Gastos Financieros')
            impuestos_base = amt(self.base_is, 'Impuestos')

            efectivo_base = amt(self.base_bs, 'Efectivo')
            cxc_base = amt(self.base_bs, 'Cuentas por Cobrar')
            inventarios_base = amt(self.base_bs, 'Inventarios')
            activos_fijos_base = amt(self.base_bs, 'Activos Fijos')
            pasivos_base = sum_tipo(self.base_bs, 'Pasivo')
            patrimonio_base = sum_tipo(self.base_bs, 'Patrimonio')
            activos_totales_base = sum_tipo(self.base_bs, 'Activo')
        else:
            ventas_base = cogs_base = op_exp_base = fin_exp_base = impuestos_base = 0.0
            efectivo_base = cxc_base = inventarios_base = activos_fijos_base = pasivos_base = patrimonio_base = activos_totales_base = 0.0

        # Calcular utilidades
        net_income_curr = ventas_curr - cogs_curr - op_exp_curr - fin_exp_curr - impuestos_curr
        net_income_base = ventas_base - cogs_base - op_exp_base - fin_exp_base - impuestos_base

        # Razones de liquidez
        current_assets_curr = efectivo_curr + cxc_curr + inventarios_curr
        current_liabilities_curr = pasivos_curr
        current_assets_base = efectivo_base + cxc_base + inventarios_base
        current_liabilities_base = pasivos_base

        current_ratio_curr = (current_assets_curr / current_liabilities_curr) if current_liabilities_curr != 0 else None
        quick_ratio_curr = ((efectivo_curr + cxc_curr) / current_liabilities_curr) if current_liabilities_curr != 0 else None
        working_capital_curr = current_assets_curr - current_liabilities_curr

        current_ratio_base = (current_assets_base / current_liabilities_base) if current_liabilities_base != 0 else None
        quick_ratio_base = ((efectivo_base + cxc_base) / current_liabilities_base) if current_liabilities_base != 0 else None
        working_capital_base = current_assets_base - current_liabilities_base

        # Rentabilidad
        gross_margin_curr = ((ventas_curr - cogs_curr) / ventas_curr) if ventas_curr != 0 else None
        operating_margin_curr = ((ventas_curr - cogs_curr - op_exp_curr) / ventas_curr) if ventas_curr != 0 else None
        net_margin_curr = (net_income_curr / ventas_curr) if ventas_curr != 0 else None

        gross_margin_base = ((ventas_base - cogs_base) / ventas_base) if ventas_base != 0 else None
        operating_margin_base = ((ventas_base - cogs_base - op_exp_base) / ventas_base) if ventas_base != 0 else None
        net_margin_base = (net_income_base / ventas_base) if ventas_base != 0 else None

        # Rentabilidad sobre activos y patrimonio
        roa_curr = (net_income_curr / activos_totales_curr) if activos_totales_curr != 0 else None
        roe_curr = (net_income_curr / patrimonio_curr) if patrimonio_curr != 0 else None

        roa_base = (net_income_base / activos_totales_base) if activos_totales_base != 0 else None
        roe_base = (net_income_base / patrimonio_base) if patrimonio_base != 0 else None

        # Estructura financiera
        debt_to_equity_curr = (pasivos_curr / patrimonio_curr) if patrimonio_curr != 0 else None
        debt_to_equity_base = (pasivos_base / patrimonio_base) if patrimonio_base != 0 else None

        asset_turnover_curr = (ventas_curr / activos_totales_curr) if activos_totales_curr != 0 else None
        asset_turnover_base = (ventas_base / activos_totales_base) if activos_totales_base != 0 else None

        # Construir DataFrame de resultados
        rows = [
            ('Current Ratio', current_ratio_base, current_ratio_curr),
            ('Quick Ratio', quick_ratio_base, quick_ratio_curr),
            ('Working Capital', working_capital_base, working_capital_curr),
            ('Gross Margin', gross_margin_base, gross_margin_curr),
            ('Operating Margin', operating_margin_base, operating_margin_curr),
            ('Net Margin', net_margin_base, net_margin_curr),
            ('ROA (Return on Assets)', roa_base, roa_curr),
            ('ROE (Return on Equity)', roe_base, roe_curr),
            ('Debt to Equity', debt_to_equity_base, debt_to_equity_curr),
            ('Asset Turnover', asset_turnover_base, asset_turnover_curr),
        ]

        df = pd.DataFrame(rows, columns=['Ratio', 'Año Base', 'Año Actual'])

        # Calcular cambio % donde sea aplicable
        def pct_change(base, curr):
            try:
                if base is None or curr is None:
                    return None
                if base == 0:
                    return None
                return ((curr - base) / abs(base)) * 100
            except Exception:
                return None

        df['Cambio %'] = df.apply(lambda r: pct_change(r['Año Base'], r['Año Actual']), axis=1)

        # Formatear valores numéricos a 4 decimales por defecto (no cambiar DataFrame en profundidad)
        return df

    def _calculate_sources_uses(self):
        # Fuentes: disminución en activos, aumento en pasivos/patrimonio
        # Usos: aumento en activos, disminución en pasivos/patrimonio
        if self.base_bs is None or self.current_bs is None: return pd.DataFrame()
        
        merged = pd.merge(self.base_bs, self.current_bs, on="Cuenta", suffixes=('_Base', '_Actual'))
        merged['Diff'] = merged['Monto_Actual'] - merged['Monto_Base']
        
        sources = []
        uses = []
        
        for index, row in merged.iterrows():
            diff = row['Diff']
            # Simplified logic: We need to know if it's Asset or Liability
            # Lógica simplificada: se requiere conocer si la cuenta es Activo, Pasivo o Patrimonio
            # Se asume una columna 'Tipo' en los datos de Excel con valores 'Activo', 'Pasivo', 'Patrimonio'
            tipo = row.get('Tipo', 'Activo') 
            
            if tipo == 'Activo':
                # Para activos: disminuciones liberan recursos (fuentes), aumentos los usan
                if diff < 0: sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff > 0: uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
            else: # Pasivo / Patrimonio
                # Para pasivos/patrimonio: aumentos son fuentes, disminuciones son usos
                if diff > 0: sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff < 0: uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                
        return {'Fuentes': pd.DataFrame(sources), 'Usos': pd.DataFrame(uses)}
