import pyodbc

def crear_conexion():
    try:
        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=DESKTOP-B2AK10N;"
            "Database=ECommerce;"
            "Trusted_Connection=Yes;" # Autenticación de Windows
            "Encrypt=Yes;"
            "TrustServerCertificate=Yes;"
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Error al conectar:", e)
        return None