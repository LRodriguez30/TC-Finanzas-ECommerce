from backend.models.cuentas import Cuenta
from config import crear_conexion

class CuentaDAO:

    @staticmethod
    def obtener_por_id_vendedor(id: int) -> Cuenta | None:
        """
        Obtiene una cuenta por el id del vendedor.
        Retorna un objeto Cuenta o None si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdCuenta, IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                        NombreCuenta, CodigoCuenta, EsAfectable,
                        EsCuentaDeSistema, Descripcion, SaldoActual
                FROM Cuentas
                WHERE IdVendedor = ?
            """, (id))
            
            row = cursor.fetchone()
            if not row:
                return None

            # Mapear los campos de la fila a un objeto Cuentas usando índices
            return Cuenta(
                id=row[0],                  # IdCuenta
                id_tipo_cuenta=row[1],      # IdTipoCuenta
                id_vendedor=row[2],         # IdVendedor
                es_cuenta_plataforma=[3],   # EsCuentaPlataforma
                nombre_cuenta=[4],          # NombreCuenta
                codigo_cuenta=[5],          # CodigoCuenta
                es_afectable=[6],           # EsAfectable
                es_cuenta_de_sistema=[7],   # EsCuentaDeSistema
                descripcion=[8],            # Descripcion
                saldo_actual=[9]            # SaldoActual
            )
        except Exception as e:
            print("Error al obtener la cuenta:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insertar_cuenta(cuenta: Cuenta) -> bool:
        """
        Inserta una cuenta en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                                    NombreCuenta, CodigoCuenta, EsAfectable,
                                    EsCuentaDeSistema, Descripcion, SaldoActual)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cuenta.id_tipo_cuenta,
                cuenta.id_vendedor,
                cuenta.es_cuenta_plataforma,
                cuenta.nombre_cuenta,
                cuenta.codigo_cuenta,
                cuenta.es_afectable,
                cuenta.es_cuenta_de_sistema,
                cuenta.descripcion,
                cuenta.saldo_actual
            ))
            conn.commit()
            return True
        except Exception as e:
            print("Error al insertar la cuenta:", e)
            return False
        finally:
            conn.close()
            
    @staticmethod
    def actualizar_cuenta(cuenta: Cuenta) -> bool:
        """
        Actualiza los datos de una cuenta existente.
        Retorna True si la actualización fue exitosa, False si falló.
        """
        conn = crear_conexion()
        if conn is None:
            print("No hay conexión con SQL Server.")
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Cuentas
                SET 
                    IdTipoCuenta = ?,
                    IdVendedor = ?,
                    EsCuentaPlataforma = ?,
                    NombreCuenta = ?,
                    CodigoCuenta = ?,
                    EsAfectable = ?,
                    EsCuentaDeSistema = ?,
                    Descripcion = ?,
                    SaldoActual = ?
                WHERE IdCuenta = ?
            """, (
                cuenta.id_tipo_cuenta,
                cuenta.id_vendedor,
                cuenta.es_cuenta_plataforma,
                cuenta.nombre_cuenta,
                cuenta.codigo_cuenta,
                cuenta.es_afectable,
                cuenta.es_cuenta_de_sistema,
                cuenta.descripcion,
                cuenta.saldo_actual,
                cuenta.id  # importante!
            ))

            conn.commit()
            return cursor.rowcount > 0  # True si una fila fue actualizada

        except Exception as e:
            print("Error al actualizar la cuenta:", e)
            return False

        finally:
            conn.close()