from backend.models.vendedores import Vendedor
from config import crear_conexion

class VendedorDAO:

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Vendedor | None:
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
            """, (id_usuario,))  # Nota la coma para tupla

            row = cursor.fetchone()
            if not row:
                return None

            return Vendedor(
                id=row[0],
                id_usuario=row[1],
                nombre_negocio=row[2],
                logo_negocio=row[3],
                descripcion_negocio=row[4],
                es_contribuyente=row[5]
            )
        except Exception as e:
            print("Error al obtener el vendedor:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_vendedor(vendedor: Vendedor) -> bool:
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
                vendedor.logo_negocio,
                vendedor.descripcion_negocio,
                vendedor.es_contribuyente
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar el vendedor:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar_vendedor(vendedor: Vendedor) -> bool:
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Vendedores
                SET NombreNegocio = ?, LogoNegocio = ?, DescripcionNegocio = ?, EsContribuyente = ?
                WHERE IdVendedor = ?
            """, (
                vendedor.nombre_negocio,
                vendedor.logo_negocio,
                vendedor.descripcion_negocio,
                vendedor.es_contribuyente,
                vendedor.id
            ))

            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error al actualizar vendedor:", e)
            return False
        finally:
            conn.close()
