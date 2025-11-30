from backend.services.cuentasService import CuentaService

class CuentaController:
    def __init__(self):
        self.service = CuentaService()

    def obtener_cuentas(self, id_vendedor: int):
        """
        Obtiene todas las cuentas de un vendedor.
        """
        resultado = self.service.obtener_cuentas(id_vendedor)
        if resultado['exito']:
            return resultado['cuentas'], None
        else:
            return [], resultado['mensajes'].get('general', 'Error al obtener cuentas')

    def registrar_cuenta(self, datos: dict):
        """
        Registra una nueva cuenta.
        """
        resultado = self.service.registrar_cuenta(datos)
        if resultado['exito']:
            return True, resultado['mensajes'].get('general', 'Cuenta creada exitosamente')
        else:
            return False, resultado['mensajes'].get('general', 'Error al crear cuenta')

    def actualizar_cuenta(self, datos: dict):
        """
        Actualiza una cuenta existente.
        """
        resultado = self.service.actualizar_cuenta(datos)
        if resultado['exito']:
            return True, resultado['mensajes'].get('general', 'Cuenta actualizada correctamente')
        else:
            return False, resultado['mensajes'].get('general', 'Error al actualizar cuenta')
