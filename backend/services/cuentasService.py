from backend.DAOs.CuentasDAO import CuentaDAO
from backend.models.cuentas import Cuenta

class CuentaService:

    def obtener_cuentas(self, id_vendedor: int):
        cuentas = CuentaDAO.obtener_por_id_vendedor(id_vendedor)

        if not cuentas:
            return {'exito': False, 'mensajes': {'general': 'No se encontraron cuentas'}}

        return {'exito': True, 'cuentas': cuentas}

    def registrar_cuenta(self, datos: dict):
        mensajes = {}

        obligatorios = ["id_tipo_cuenta", "id_vendedor", "nombre_cuenta", "codigo_cuenta"]
        for campo in obligatorios:
            if not datos.get(campo):
                mensajes[campo] = f"El campo {campo} es obligatorio."

        if mensajes:
            primer_error = next(iter(mensajes.values()))
            return {'exito': False, 'mensajes': {'general': primer_error}}

        cuenta = Cuenta(
            id_tipo_cuenta=datos["id_tipo_cuenta"],
            id_vendedor=datos["id_vendedor"],
            es_cuenta_plataforma=bool(datos.get("es_cuenta_plataforma", False)),
            nombre_cuenta=datos["nombre_cuenta"],
            codigo_cuenta=datos["codigo_cuenta"],
            es_afectable=bool(datos.get("es_afectable", True)),
            es_cuenta_de_sistema=bool(datos.get("es_cuenta_de_sistema", False)),
            descripcion=datos.get("descripcion", ""),
            saldo_actual=float(datos.get("saldo_actual", 0.0))
        )

        exito = CuentaDAO.insertar_cuenta(cuenta)

        if exito:
            return {'exito': True, 'mensajes': {'general': 'Cuenta creada exitosamente'}}
        else:
            return {'exito': False, 'mensajes': {'general': 'Error al crear cuenta'}}

    def actualizar_cuenta(self, datos: dict):
        """
        Actualiza una cuenta existente. Se espera que 'id' esté en datos.
        """
        if not datos.get("id"):
            return {'exito': False, 'mensajes': {'general': 'ID de cuenta requerido'}}

        cuenta = Cuenta(
            id=datos["id"],
            id_tipo_cuenta=datos.get("id_tipo_cuenta"),
            id_vendedor=datos.get("id_vendedor"),
            es_cuenta_plataforma=bool(datos.get("es_cuenta_plataforma", False)),
            nombre_cuenta=datos.get("nombre_cuenta"),
            codigo_cuenta=datos.get("codigo_cuenta"),
            es_afectable=bool(datos.get("es_afectable", True)),
            es_cuenta_de_sistema=bool(datos.get("es_cuenta_de_sistema", False)),
            descripcion=datos.get("descripcion", ""),
            saldo_actual=float(datos.get("saldo_actual", 0.0))
        )

        exito = CuentaDAO.actualizar_cuenta(cuenta)

        if exito:
            return {'exito': True, 'mensajes': {'general': 'Cuenta actualizada correctamente'}}
        else:
            return {'exito': False, 'mensajes': {'general': 'Error al actualizar la cuenta'}}
