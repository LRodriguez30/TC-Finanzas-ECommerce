from backend.services.usuariosService import UsuarioService

class UsuarioController:
    def __init__(self):
        self.service = UsuarioService()

    def registrar(self, datos):
        resultado = self.service.registrar(datos)
        if resultado['exito']:
            return True, resultado['mensajes'].get('general', "Registro exitoso")
        else:
            # Tomar solo el primer mensaje de error
            primer_error = next(iter(resultado['mensajes'].values()))
            return False, primer_error

    def login(self, correo, contraseña):
        resultado = self.service.login(correo, contraseña)
        if resultado['exito']:
            return resultado['usuario'], None
        else:
            # Tomar solo el primer mensaje de error
            primer_error = next(iter(resultado['mensajes'].values()))
            return None, primer_error

