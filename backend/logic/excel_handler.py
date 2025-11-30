import pandas as pd
import os

class ExcelHandler:
    @staticmethod
    def generate_templates(directory):
        # Plantilla de Balance General
        # Crea una plantilla básica con filas típicas de cuentas (activo, pasivo, patrimonio)
        # y columnas requeridas para que el usuario complete los montos.
        bs_data = {
            'Cuenta': ['Efectivo', 'Cuentas por Cobrar', 'Inventarios', 'Activos Fijos', 'Cuentas por Pagar', 'Deuda Largo Plazo', 'Capital Social', 'Utilidades Retenidas'],
            'Tipo': ['Activo', 'Activo', 'Activo', 'Activo', 'Pasivo', 'Pasivo', 'Patrimonio', 'Patrimonio'],
            'Monto': [0, 0, 0, 0, 0, 0, 0, 0]
        }
        bs_df = pd.DataFrame(bs_data)
        
        
        is_data = {
            'Cuenta': ['Ventas Netas', 'Costo de Ventas', 'Gastos Operativos', 'Gastos Financieros', 'Impuestos'],
            'Tipo': ['Ingreso', 'Egreso', 'Egreso', 'Egreso', 'Egreso'],
            'Monto': [0, 0, 0, 0, 0]
        }
        is_df = pd.DataFrame(is_data)
        
        # Crea un archivo Excel único con dos hojas (Balance General y Estado de Resultados)
        # para que el usuario descargue y complete los datos financieros.
        output_path = os.path.join(directory, "Plantilla_Financiera.xlsx")
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            bs_df.to_excel(writer, sheet_name='Balance General', index=False)
            is_df.to_excel(writer, sheet_name='Estado Resultados', index=False)

    @staticmethod
    def load_financial_data(file_path):
        # Carga datos financieros desde un archivo Excel
        # Se espera que el archivo contenga las hojas "Balance General" y "Estado Resultados",
        # o que el usuario suba un único archivo con ambas hojas. En implementaciones más
        # avanzadas podría aceptarse la carga por separado o validarse la estructura.
        try:
            bs = pd.read_excel(file_path, sheet_name='Balance General')
            iss = pd.read_excel(file_path, sheet_name='Estado Resultados')
            return bs, iss
        except Exception as e:
            print(f"Error al cargar Excel: {e}")
            return None, None
