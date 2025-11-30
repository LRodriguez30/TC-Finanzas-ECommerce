from backend.models.usuarios import Usuario
from backend.DAOs.UsuariosDAO import UsuarioDAO

from utils.helpers import encriptar_contraseña, verificar_contraseña
import re

class UsuarioService:
    def login(self, correo: str, contraseña: str):
        mensajes = {}

        # Validaciones básicas
        if not correo:
            mensajes['correo'] = "El correo es obligatorio."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            mensajes['correo'] = "El correo no tiene un formato válido."

        if not contraseña:
            mensajes['contraseña'] = "La contraseña es obligatoria."

        if mensajes:
            return {'exito': False, 'usuario': None, 'mensajes': mensajes}

        usuario = UsuarioDAO.obtener_por_correo(correo)

        # Verificamos que exista usuario y que tenga contraseña
        if not usuario or not usuario.contraseña:
            mensajes['general'] = "Correo o contraseña incorrectos"
            return {'exito': False, 'mensajes': mensajes}

        # Validamos la contraseña con bcrypt
        if not verificar_contraseña(contraseña, usuario.contraseña):
            mensajes['general'] = "Correo o contraseña incorrectos"
            return {'exito': False, 'mensajes': mensajes}

        return {'exito': True, 'usuario': usuario, 'mensajes': {}}

    def registrar(self, datos: dict):
        mensajes = {}

        nombres_interfaz = {
            "id_rol": "rol",
            "primer_nombre": "primer nombre",
            "segundo_nombre": "segundo nombre",
            "primer_apellido": "primer apellido",
            "segundo_apellido": "segundo apellido",
            "telefono": "teléfono",
            "correo": "correo electrónico",
            "contraseña": "contraseña"
        }

        obligatorios = ["id_rol", "primer_nombre", "primer_apellido",
                        "telefono", "correo", "contraseña"]
        for campo in obligatorios:
            if not datos.get(campo):
                mensajes[campo] = f"El {nombres_interfaz[campo]} es obligatorio."

        # Validaciones adicionales
        if 'correo' in datos and datos['correo']:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", datos['correo']):
                mensajes['correo'] = "El correo no tiene un formato válido."
            elif UsuarioDAO.obtener_por_correo(datos['correo']):
                mensajes['correo'] = "Este correo ya está registrado."

        if 'telefono' in datos and datos['telefono']:
            if not re.match(r"^\+?\d{7,15}$", datos['telefono']):
                mensajes['telefono'] = "Número de teléfono no válido."

        if 'contraseña' in datos and datos['contraseña']:
            if len(datos['contraseña']) < 6:
                mensajes['contraseña'] = "La contraseña debe tener al menos 6 caracteres."

        # Validar que contraseña y confirmación coincidan
        if datos.get("contraseña") != datos.get("confirmar_contraseña"):
            mensajes["confirmar_contraseña"] = "Las contraseñas no coinciden."

        if mensajes:
            # Solo retornamos el primer mensaje
            primer_error = next(iter(mensajes.values()))
            return {'exito': False, 'mensajes': {"general": primer_error}}

        # Crear usuario con contraseña hasheada
        usuario = Usuario(
            id_rol=datos["id_rol"],
            primer_nombre=datos["primer_nombre"],
            segundo_nombre=datos.get("segundo_nombre"),
            primer_apellido=datos["primer_apellido"],
            segundo_apellido=datos.get("segundo_apellido"),
            telefono=datos["telefono"],
            correo=datos["correo"],
            contraseña=encriptar_contraseña(datos["contraseña"])
        )

        exito = UsuarioDAO.insertar_usuario(usuario)
        if exito:
            return {'exito': True, 'mensajes': {"general": "Registro exitoso."}}
        else:
            return {'exito': False, 'mensajes': {"general": "Error al registrar usuario."}}