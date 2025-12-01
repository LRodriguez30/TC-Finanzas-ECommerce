from backend.models.cuentas import Cuenta
from config import crear_conexion

class CuentaDAO:

    @staticmethod
    def obtener_cuentas_balance_plataforma() -> list[Cuenta]:
        conn = crear_conexion()
        if conn is None:
            return []
        
        try:
            cursor = conn.cursor()
            # Asumimos que 1,2,3,4,5 son cuentas de Balance (Activo, Pasivo, Capital)
            # Basado en el input del usuario: 1=Efectivo(Activo?), 2=Mobiliario(Activo?), 5=Capital
            cursor.execute("""
                SELECT IdCuenta, IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                        NombreCuenta, CodigoCuenta, EsAfectable,
                        EsCuentaDeSistema, Descripcion, SaldoActual
                FROM Cuentas
                WHERE EsCuentaPlataforma = 1 AND IdTipoCuenta IN (1, 2, 3, 4, 5)
            """)

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
            print("Error al obtener las cuentas de balance de plataforma:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_cuentas_resultados_plataforma() -> list[Cuenta]:
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
                WHERE EsCuentaPlataforma = 1 AND IdTipoCuenta IN (6, 7)
            """)

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
            print("Error al obtener las cuentas de resultados de plataforma:", e)
            return []
        finally:
            conn.close()

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

    @staticmethod
    def vendedor_tiene_cuentas(id_vendedor: int) -> bool:
        """
        Verifica si un vendedor tiene al menos una cuenta creada.
        Retorna True si tiene cuentas, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM Cuentas
                WHERE IdVendedor = ?
            """, (id_vendedor,))
            
            count = cursor.fetchone()[0]
            return count > 0
        
        except Exception as e:
            print("Error al verificar cuentas del vendedor:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def crear_cuentas_esenciales_vendedor(id_vendedor: int) -> bool:
        """
        Crea las cuentas esenciales del sistema para un vendedor:
        - Ingresos (Tipo 6)
        - Efectivo (Tipo 1 - Activo Corriente)
        - Capital Social (Tipo 5 - Capital)
        - Utilidades Retenidas (Tipo 5 - Capital)
        - Gastos de Ventas (Tipo 7 - Gasto Operativo)
        
        Retorna True si se crearon correctamente, False en caso contrario.
        """
        import random
        
        conn = crear_conexion()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Definir las cuentas esenciales
            cuentas_esenciales = [
                {
                    "nombre": "Ingresos",
                    "tipo": 6,  # Ingreso
                    "codigo": f"{random.randint(1000, 9999)}",
                    "descripcion": "Cuenta de ingresos del negocio"
                },
                {
                    "nombre": "Efectivo",
                    "tipo": 1,  # Activo Corriente
                    "codigo": f"{random.randint(1000, 9999)}",
                    "descripcion": "Efectivo disponible"
                },
                {
                    "nombre": "Capital Social",
                    "tipo": 5,  # Capital
                    "codigo": f"{random.randint(1000, 9999)}",
                    "descripcion": "Capital aportado por el propietario"
                },
                {
                    "nombre": "Utilidades Retenidas",
                    "tipo": 5,  # Capital
                    "codigo": f"{random.randint(1000, 9999)}",
                    "descripcion": "Utilidades acumuladas no distribuidas"
                },
                {
                    "nombre": "Gastos de Ventas",
                    "tipo": 7,  # Gasto Operativo
                    "codigo": f"{random.randint(1000, 9999)}",
                    "descripcion": "Gastos relacionados con ventas"
                }
            ]
            
            # Insertar cada cuenta
            for cuenta in cuentas_esenciales:
                cursor.execute("""
                    INSERT INTO Cuentas (
                        IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                        NombreCuenta, CodigoCuenta, EsAfectable,
                        EsCuentaDeSistema, Descripcion, SaldoActual
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cuenta["tipo"],
                    id_vendedor,
                    0,  # No es cuenta de plataforma
                    cuenta["nombre"],
                    cuenta["codigo"],
                    1,  # Es afectable
                    1,  # Es cuenta de sistema
                    cuenta["descripcion"],
                    0.0  # Saldo inicial 0
                ))
            
            conn.commit()
            return True
        
        except Exception as e:
            print("Error al crear cuentas esenciales del vendedor:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar_saldos(id_cuenta1: int, monto1: float, id_cuenta2: int, monto2: float) -> bool:
        """
        Actualiza los saldos de dos cuentas siguiendo la partida doble.
        
        Args:
            id_cuenta1: ID de la primera cuenta
            monto1: Monto a sumar/restar de la primera cuenta (puede ser positivo o negativo)
            id_cuenta2: ID de la segunda cuenta
            monto2: Monto a sumar/restar de la segunda cuenta (puede ser positivo o negativo)
        
        Returns:
            True si se actualizaron correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Actualizar primera cuenta
            cursor.execute("""
                UPDATE Cuentas
                SET SaldoActual = SaldoActual + ?
                WHERE IdCuenta = ?
            """, (monto1, id_cuenta1))
            
            # Actualizar segunda cuenta
            cursor.execute("""
                UPDATE Cuentas
                SET SaldoActual = SaldoActual + ?
                WHERE IdCuenta = ?
            """, (monto2, id_cuenta2))
            
            conn.commit()
            return True
        
        except Exception as e:
            print("Error al actualizar saldos:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def verificar_nombre_duplicado(id_vendedor: int, nombre_cuenta: str) -> bool:
        """
        Verifica si ya existe una cuenta con el mismo nombre para el vendedor.
        Retorna True si existe duplicado, False si no existe.
        """
        conn = crear_conexion()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM Cuentas
                WHERE IdVendedor = ? AND NombreCuenta = ?
            """, (id_vendedor, nombre_cuenta))
            
            count = cursor.fetchone()[0]
            return count > 0
        
        except Exception as e:
            print("Error al verificar nombre duplicado:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def insertar_cuenta(cuenta: Cuenta) -> bool:
        """
        Inserta una nueva cuenta en la base de datos.
        Retorna True si se insertó correctamente, False en caso contrario.
        """
        conn = crear_conexion()
        if conn is None:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cuentas (
                    IdTipoCuenta, IdVendedor, EsCuentaPlataforma,
                    NombreCuenta, CodigoCuenta, EsAfectable,
                    EsCuentaDeSistema, Descripcion, SaldoActual
                )
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
            print("Error al insertar cuenta:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
