from backend.models.usuarios import Usuario
from config import crear_conexion

class UsuarioDAO:

    @staticmethod
    def obtener_por_correo(correo: str) -> Usuario | None:
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
                SELECT IdUsuario, IdRol, PrimerNombre, SegundoNombre,
                PrimerApellido, SegundoApellido, Telefono, Correo,
                Contraseña, FechaRegistro
                FROM Usuarios
                WHERE Correo = ?
            """, (correo))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Usuario usando índices
            return Usuario(
                id=row[0],                # IdUsuario
                id_rol=row[1],            # IdRol
                primer_nombre=row[2],     # PrimerNombre
                segundo_nombre=row[3],    # SegundoNombre
                primer_apellido=row[4],   # PrimerApellido
                segundo_apellido=row[5],  # SegundoApellido
                telefono=row[6],          # Telefono
                correo=row[7],            # Correo
                contraseña=row[8],        # <-- hash de bcrypt
                fecha_registro=row[9]     # FechaRegistro
            )
        except Exception as e:
            print("Error al obtener usuario:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_usuario(usuario: Usuario) -> bool:
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
                INSERT INTO Usuarios (IdRol, PrimerNombre, SegundoNombre,
                PrimerApellido, SegundoApellido,
                Telefono, Correo, Contraseña)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario.id_rol,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                usuario.correo,
                usuario.contraseña  # <-- hash bcrypt
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar usuario:", e)
            return False
        finally:
            conn.close()
