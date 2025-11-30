from backend.models.administradores import Administrador
from config import crear_conexion

class AdministradorDAO:

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Administrador | None:
        """
        Obtiene un administrador por su id de usuario.
        Retorna un objeto Administrador o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdAdministrador, IdUsuario
                FROM Administradores
                WHERE IdUsuario = ?
            """, (id_usuario))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Administrador usando índices
            return Administrador(
                id=row[0],                  # IdAdministrador
                id_usuario=row[1]           # IdUsuario
            )
        except Exception as e:
            print("Error al obtener el comprador:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_administrador(administrador: Administrador) -> bool:
        """
        Inserta un administrador en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Administradores (IdUsuario)
                VALUES (?)
            """, (
                administrador.id_usuario
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar el administrador:", e)
            return False
        finally:
            conn.close()