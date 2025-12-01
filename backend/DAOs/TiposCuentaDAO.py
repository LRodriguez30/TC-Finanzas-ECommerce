from backend.db.connection import crear_conexion
from backend.models.tiposDeCuenta import TipoDeCuenta

class TiposCuentaDAO:
    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los tipos de cuenta de la base de datos.
        Retorna una lista de objetos TipoDeCuenta.
        """
        conn = crear_conexion()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT IdTipoCuenta, Nombre, Categoria, Descripcion FROM TiposDeCuenta")
            rows = cursor.fetchall()
            
            tipos = []
            for row in rows:
                tipos.append(TipoDeCuenta(
                    id_tipo_cuenta=row[0],
                    nombre=row[1],
                    categoria=row[2],
                    descripcion=row[3]
                ))
            return tipos
        
        except Exception as e:
            print(f"Error al obtener tipos de cuenta: {e}")
            return []
        finally:
            conn.close()
