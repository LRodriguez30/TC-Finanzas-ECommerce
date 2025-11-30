from backend.controllers.controladorUsuarios import UsuarioController
from frontend.components.navigation import ir_a_pagina_principal, ir_a_login
import customtkinter as ctk

controlador = UsuarioController()

def registrar(datos: dict, etiqueta_mensaje: ctk.CTkLabel, ventana: ctk.CTk, marco: ctk.CTkFrame) -> None:
    """
    Intenta registrar un usuario usando los datos proporcionados.
    Muestra el resultado en la etiqueta_mensaje y redirige al login si es exitoso.
    """
    exito, mensaje = controlador.registrar(datos)
    etiqueta_mensaje.configure(text=mensaje, text_color="green" if exito else "red")
    if exito:
        ir_a_pagina_principal(ventana, marco, datos)  # Redirige al login tras registro exitoso

def iniciar_sesion(correo: str, contraseña: str, etiqueta_mensaje: ctk.CTkLabel, ventana: ctk.CTk, marco: ctk.CTkFrame) -> None:
    """
    Intenta iniciar sesión con el correo y la contraseña proporcionados.
    Redirige a la página principal si es exitoso, muestra error en etiqueta_mensaje si falla.
    """
    usuario, error = controlador.login(correo, contraseña)
    if usuario:
        ir_a_pagina_principal(ventana, marco, usuario)
    else:
        etiqueta_mensaje.configure(text=error or "Correo o contraseña incorrectos", text_color="red")

def limpiar_mensaje(etiqueta_mensaje: ctk.CTkLabel):
    """
    Retorna una función que limpia el mensaje de la etiqueta.
    Se puede usar en un bind de Entry:
        entry.bind("<Key>", limpiar_mensaje(etiqueta_mensaje))
    """
    def limpiar(event) -> None:
        etiqueta_mensaje.configure(text="")
    return limpiar

