from backend.models.transacciones import Transaccion
from config import crear_conexion

class TransaccionDAO:

    @staticmethod
    def obtener_exacta(
        id_producto: int,
        id_comprador: int,
        id_vendedor: int
    ) -> Transaccion | None:
        """
        Obtiene una transacción especifica.
        Retorna un objeto Transaccion o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdTransaccion, IdProducto, IdComprador, IdVendedor,
                       IdEstadoTransaccion, IdMetodoPago, PrecioUnitario,
                       UnidadesCompradas, PrecioEnvio, Descuento,
                       PrecioTotal, CostoUnitario, Fecha
                FROM Transacciones
                WHERE IdProducto = ?
                AND IdComprador = ?
                AND Vendedor = ?
            """, (
                id_producto,
                id_comprador,
                id_vendedor
            ))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Producto usando índices
            return Transaccion(
                id=row[0],                   # IdTransaccion
                id_vendedor=row[1],          # IdProducto
                id_categoria=row[2],         # IdComprador
                id_estado_producto=row[3],   # IdEstadoProducto
                nombre=row[4],               # Nombre
                precio=row[5],               # Precio
                descripcion=row[6],          # Descripcion
                stock_disponible=row[7],     # StockDisponible
                fecha_publicacion=row[8],    # FechaPublicacion
            )
        except Exception as e:
            print("Error al obtener la transacción:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_transaccion(transaccion: Transaccion) -> bool:
        """
        Inserta una transacción en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (IdProducto, IdComprador, IdVendedor,
                                      IdEstadoTransaccion, IdMetodoDePago,
                                      PrecioUnitario, UnidadesCompradas,
                                      PrecioEnvio, Descuento, PrecioTotal,
                                      CostoUnitario, Fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaccion.id_producto,
                transaccion.id_comprador,
                transaccion.id_vendedor,
                transaccion.id_estado_transaccion,
                transaccion.id_metodo_pago,
                transaccion.precio_unitario,
                transaccion.unidades_compradas,
                transaccion.precio_envio,
                transaccion.descuento,
                transaccion.precio_total,
                transaccion.costo_unitario,
                transaccion.fecha
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar la transacción:", e)
            return False
        finally:
            conn.close()