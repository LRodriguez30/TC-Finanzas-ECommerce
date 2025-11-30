import pandas as pd
import os

class ExcelHandler:
    @staticmethod
    def generate_templates(directory):
        # Balance Sheet Template
        bs_data = {
            'Cuenta': ['Efectivo', 'Cuentas por Cobrar', 'Inventarios', 'Activos Fijos', 'Cuentas por Pagar', 'Deuda Largo Plazo', 'Capital Social', 'Utilidades Retenidas'],
            'Tipo': ['Activo', 'Activo', 'Activo', 'Activo', 'Pasivo', 'Pasivo', 'Patrimonio', 'Patrimonio'],
            'Monto': [0, 0, 0, 0, 0, 0, 0, 0]
        }
        bs_df = pd.DataFrame(bs_data)
        
        # Income Statement Template
        is_data = {
            'Cuenta': ['Ventas Netas', 'Costo de Ventas', 'Gastos Operativos', 'Gastos Financieros', 'Impuestos'],
            'Tipo': ['Ingreso', 'Egreso', 'Egreso', 'Egreso', 'Egreso'],
            'Monto': [0, 0, 0, 0, 0]
        }
        is_df = pd.DataFrame(is_data)
        
        # Create a single Excel file with two sheets
        output_path = os.path.join(directory, "Plantilla_Financiera.xlsx")
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            bs_df.to_excel(writer, sheet_name='Balance General', index=False)
            is_df.to_excel(writer, sheet_name='Estado Resultados', index=False)

    @staticmethod
    def load_financial_data(file_path):
        # Expects sheets "Balance General" and "Estado Resultados" or separate files
        # For simplicity, let's assume the user uploads one file with 2 sheets
        try:
            bs = pd.read_excel(file_path, sheet_name='Balance General')
            iss = pd.read_excel(file_path, sheet_name='Estado Resultados')
            return bs, iss
        except Exception as e:
            print(f"Error loading Excel: {e}")
            return None, None
