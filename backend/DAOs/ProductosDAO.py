from backend.models.productos import Producto
from config import crear_conexion

class ProductoDAO:

    @staticmethod
    def obtener_por_id_vendedor(id: int) -> Producto | None:
        """
        Obtiene un producto por el id del vendedor.
        Retorna un objeto Producto o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdProducto, IdVendedor, IdCategoria, IdEstadoProducto,
                       Nombre, Precio, Descripcion, StockDisponible,
                       FechaPublicacion
                FROM Productos
                WHERE IdVendedor = ?
            """, (id))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Producto usando índices
            return Producto(
                id=row[0],                   # IdProducto
                id_vendedor=row[1],          # IdVendedor
                id_categoria=row[2],         # IdCategoria
                id_estado_producto=row[3],   # IdEstadoProducto
                nombre=row[4],               # Nombre
                precio=row[5],               # Precio
                descripcion=row[6],          # Descripcion
                stock_disponible=row[7],     # StockDisponible
                fecha_publicacion=row[8],    # FechaPublicacion
            )
        except Exception as e:
            print("Error al obtener el producto:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_producto(producto: Producto) -> bool:
        """
        Inserta un producto en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (IdVendedor, IdCategoria, IdEstadoProducto,
                                      Nombre, Precio, Descripcion,
                                      StockDisponible, FechaPublicacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                producto.id_vendedor,
                producto.id_categoria,
                producto.id_estado_producto,
                producto.nombre,
                producto.precio,
                producto.descripcion,
                producto.stock_disponible,
                producto.fecha_publicacion
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar el producto:", e)
            return False
        finally:
            conn.close()