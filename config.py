try:
    import pyodbc
    _HAS_PYODBC = True
except Exception:
    pyodbc = None
    _HAS_PYODBC = False
    print("Aviso: 'pyodbc' no está instalado. Para habilitar conexión a SQL Server instala 'pyodbc'.")
    print("Instalación sugerida:")
    print("  pip install pyodbc")
    print("En Windows puede requerir Build Tools; alternativa: 'pipwin install pyodbc' o usar conda: 'conda install -c anaconda pyodbc'")


def crear_conexion():
    """Crea una conexión a SQL Server usando ODBC.

    Si 'pyodbc' no está disponible, devuelve None y no lanza excepción.
    """
    if not _HAS_PYODBC:
        print("No se puede crear conexión: falta el paquete 'pyodbc'.")
        return None

    try:
        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=RAFAELESPINOZA\\SQLSERVER2019;"
            "Database=ECommerce;"
            "Trusted_Connection=Yes;"  # Autenticación de Windows
            "Encrypt=Yes;"
            "TrustServerCertificate=Yes;"
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Error al conectar a SQL Server:", e)
        return None