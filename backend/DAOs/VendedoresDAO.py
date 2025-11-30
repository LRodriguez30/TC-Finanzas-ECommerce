from backend.models.vendedores import Vendedor
from config import crear_conexion

class VendedorDAO:

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Vendedor | None:
        """
        Obtiene un vendedor por su id de usuario.
        Retorna un objeto Vendedor o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdVendedor, IdUsuario, NombreNegocio, LogoNegocio,
                       DescripcionNegocio, EsContribuyente
                FROM Vendedores
                WHERE IdUsuario = ?
            """, (id_usuario))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Vendedor usando índices
            return Vendedor(
                id=row[0],                   # IdVendedor
                id_usuario=row[1],           # IdUsuario
                nombre_negocio=row[2],       # NombreNegocio
                logo_negocio=row[3],         # LogoNegocio
                descripcion_negocio=row[4],  # DescripcionNegocio
                es_contribuyente=row[5],     # EsContribuyente
            )
        except Exception as e:
            print("Error al obtener el vendedor:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_vendedor(vendedor: Vendedor) -> bool:
        """
        Inserta un vendedor en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Vendedores (IdUsuario, NombreNegocio, LogoNegocio,
                                      DescripcionNegocio, EsContribuyente)
                VALUES (?, ?, ?, ?, ?)
            """, (
                vendedor.id_usuario,
                vendedor.nombre_negocio,
                vendedor.descripcion_negocio,
                vendedor.logo_negocio,
                vendedor.es_contribuyente
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar el vendedor:", e)
            return False
        finally:
            conn.close()