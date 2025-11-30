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

    @staticmethod
    def obtener_por_id(id_usuario: int) -> Usuario | None:
        """
        Obtiene un usuario por su IdUsuario.
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
                WHERE IdUsuario = ?
            """, (id_usuario,))
            row = cursor.fetchone()
            if not row:
                return None

            return Usuario(
                id=row[0],
                id_rol=row[1],
                primer_nombre=row[2],
                segundo_nombre=row[3],
                primer_apellido=row[4],
                segundo_apellido=row[5],
                telefono=row[6],
                correo=row[7],
                contraseña=row[8],
                fecha_registro=row[9]
            )
        except Exception as e:
            print("Error al obtener usuario por id:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar_correo(id_usuario: int, nuevo_correo: str) -> bool:
        """Actualiza el correo de un usuario dado su id."""
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Usuarios SET Correo = ? WHERE IdUsuario = ?
            """, (nuevo_correo, id_usuario))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar correo:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar_contraseña(id_usuario: int, hashed_password: str) -> bool:
        """Actualiza la contraseña hasheada del usuario."""
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Usuarios SET Contraseña = ? WHERE IdUsuario = ?
            """, (hashed_password, id_usuario))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar contraseña:", e)
            return False
        finally:
            conn.close()
