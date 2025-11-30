from backend.models.compradores import Comprador
from config import crear_conexion

class CompradorDAO:

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Comprador | None:
        """
        Obtiene un comprador por su id de usuario.
        Retorna un objeto Comprador o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdComprador, IdUsuario
                FROM Compradores
                WHERE IdUsuario = ?
            """, (id_usuario))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Administrador usando índices
            return Comprador(
                id=row[0],                  # IdComprador
                id_usuario=row[1]           # IdUsuario
            )
        except Exception as e:
            print("Error al obtener el comprador:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_comprador(comprador: Comprador) -> bool:
        """
        Inserta un usuario en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Compradores (IdUsuario)
                VALUES (?)
            """, (
                comprador.id_usuario
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar el comprador:", e)
            return False
        finally:
            conn.close()