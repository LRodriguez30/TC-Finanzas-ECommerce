from backend.models.cuentas import Cuenta
from config import crear_conexion

class CuentaDAO:

    @staticmethod
    def obtener_por_id_vendedor(id_vendedor: int) -> list[Cuenta]:
        conn = crear_conexion()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT IdCuenta, IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                        NombreCuenta, CodigoCuenta, EsAfectable,
                        EsCuentaDeSistema, Descripcion, SaldoActual
                FROM Cuentas
                WHERE IdVendedor = ?
            """, (id_vendedor,))  # tupla de un solo elemento

            rows = cursor.fetchall()
            cuentas = []

            for row in rows:
                cuentas.append(
                    Cuenta(
                        id=row[0],
                        id_tipo_cuenta=row[1],
                        id_vendedor=row[2],
                        es_cuenta_plataforma=row[3],
                        nombre_cuenta=row[4],
                        codigo_cuenta=row[5],
                        es_afectable=row[6],
                        es_cuenta_de_sistema=row[7],
                        descripcion=row[8],
                        saldo_actual=row[9]
                    )
                )

            return cuentas

        except Exception as e:
            print("Error al obtener las cuentas:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def insertar_cuenta(cuenta: Cuenta) -> bool:
        conn = crear_conexion()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cuentas (IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
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
                cuenta.id
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print("Error al actualizar la cuenta:", e)
            return False
        finally:
            conn.close()
