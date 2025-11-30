import pandas as pd

class FinancialAnalyzer:
    def __init__(self):
        self.base_bs = None # Balance Sheet Base Year
        self.current_bs = None # Balance Sheet Current Year
        self.base_is = None # Income Statement Base Year
        self.current_is = None # Income Statement Current Year
        
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
        # Assumes 'Monto' column exists. Calculates % of total.
        # For BS: % of Total Assets. For IS: % of Total Sales.
        if df is None or df.empty: return pd.DataFrame()
        
        result = df.copy()
        total = result['Monto'].max() # Simplification: Assume max value is the total (Assets or Sales)
        # In a real scenario, we'd look for specific rows like "TOTAL ACTIVOS" or "VENTAS NETAS"
        
        result['Vertical %'] = (result['Monto'] / total) * 100
        return result

    def _horizontal_analysis(self, base_df, current_df):
        if base_df is None or current_df is None: return pd.DataFrame()
        
        # Merge on Account Name
        merged = pd.merge(base_df, current_df, on="Cuenta", suffixes=('_Base', '_Actual'))
        merged['Variación $'] = merged['Monto_Actual'] - merged['Monto_Base']
        merged['Variación %'] = (merged['Variación $'] / merged['Monto_Base']) * 100
        return merged

    def _calculate_ratios(self):
        # Extract key values (Mock implementation - requires specific row identification)
        # For this demo, we will return the static structure but populated if data existed
        # In a real app, we need a robust mapping of "Account Name" -> "System ID"
        return []

    def _calculate_sources_uses(self):
        # Sources: Decrease in Asset, Increase in Liability/Equity
        # Uses: Increase in Asset, Decrease in Liability/Equity
        if self.base_bs is None or self.current_bs is None: return pd.DataFrame()
        
        merged = pd.merge(self.base_bs, self.current_bs, on="Cuenta", suffixes=('_Base', '_Actual'))
        merged['Diff'] = merged['Monto_Actual'] - merged['Monto_Base']
        
        sources = []
        uses = []
        
        for index, row in merged.iterrows():
            diff = row['Diff']
            # Simplified logic: We need to know if it's Asset or Liability
            # Assuming a 'Tipo' column in Excel: 'Activo', 'Pasivo', 'Patrimonio'
            tipo = row.get('Tipo', 'Activo') 
            
            if tipo == 'Activo':
                if diff < 0: sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff > 0: uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
            else: # Pasivo / Patrimonio
                if diff > 0: sources.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                elif diff < 0: uses.append({'Cuenta': row['Cuenta'], 'Monto': abs(diff)})
                
        return {'Fuentes': pd.DataFrame(sources), 'Usos': pd.DataFrame(uses)}
