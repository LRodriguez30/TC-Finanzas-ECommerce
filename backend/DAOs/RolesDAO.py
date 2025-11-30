from backend.models.roles import Rol
from config import crear_conexion

class RolDAO:

    @staticmethod
    def obtener_roles() -> Rol | None:
        """
        Obtiene los roles
        Retorna un objeto Rol o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdRol, NombreRol, Descripcion
                FROM Roles
            """)
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Producto usando índices
            return Rol(
                id=row[0],            # IdRol
                nombre_rol=row[1],    # NombreRol
                descripcion=row[2]    # Descripcion
            )
        except Exception as e:
            print("Error al obtener los roles:", e)
            return None
        finally:
            conn.close()
            
    @staticmethod
    def obtener_por_nombre_rol(nombre_rol: str) -> Rol | None:
        """
        Obtiene un usuario por su correo.
        Retorna un objeto Usuario o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdRol, NombreRol, Descripcion
                FROM Roles
                WHERE NombreRol = ?
            """, (nombre_rol))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Usuario usando índices
            return Rol(
                id=row[0],            # IdRol
                nombre_rol=row[1],    # NombreRol
                descripcion=row[2],   # Descripcion
            )
        except Exception as e:
            print("Error al obtener el rol:", e)
            return None
        finally:
            conn.close()