from backend.controllers.controladorUsuarios import UsuarioController
from frontend.components.navigation import ir_a_pagina_principal, ir_a_login
from frontend.ui.loading import mostrar_cargando
import customtkinter as ctk
import time

controlador = UsuarioController()

def registrar(datos: dict, etiqueta_mensaje: ctk.CTkLabel, ventana: ctk.CTk, marco: ctk.CTkFrame, marco_loading: ctk.CTkFrame = None) -> None:
    """
    Intenta registrar un usuario usando los datos proporcionados.
    Muestra el resultado en la etiqueta_mensaje y redirige al login si es exitoso.
    """
    if marco_loading:
        mostrar_cargando(marco_loading, "Registrando usuario...")
        # Pequeña pausa para que se vea la animación (opcional, pero ayuda a la UX si es muy rápido)
        ventana.update() 
        time.sleep(1)

    exito, mensaje = controlador.registrar(datos)
    
    if exito:
        if marco_loading:
            mostrar_cargando(marco_loading, "¡Registro exitoso!\nCargando aplicación...")
            ventana.update()
            time.sleep(1)
        
        # Obtener el usuario recién registrado de la base de datos
        from backend.DAOs.UsuariosDAO import UsuarioDAO
        usuario = UsuarioDAO.obtener_por_correo(datos["correo"])
        
        if usuario:
            ir_a_pagina_principal(ventana, marco, usuario)
        else:
            etiqueta_mensaje.configure(text="Error al cargar usuario registrado", text_color="red")
            if marco_loading:
                for widget in marco_loading.winfo_children(): widget.destroy()
    else:
        # Si falla, restaurar el frame de loading (opcional, o dejarlo y mostrar error en el form)
        # Por ahora solo mostramos el error en la etiqueta, el loading se queda o se podría limpiar
        # Si queremos restaurar el color original del loading frame:
        if marco_loading:
             # Limpiar loading y restaurar color (aunque el usuario reintentará)
             for widget in marco_loading.winfo_children(): widget.destroy()
        
        etiqueta_mensaje.configure(text=mensaje, text_color="red")

def iniciar_sesion(correo: str, contraseña: str, etiqueta_mensaje: ctk.CTkLabel, ventana: ctk.CTk, marco: ctk.CTkFrame, marco_loading: ctk.CTkFrame = None) -> None:
    """
    Intenta iniciar sesión con el correo y la contraseña proporcionados.
    Redirige a la página principal si es exitoso, muestra error en etiqueta_mensaje si falla.
    """
    if marco_loading:
        mostrar_cargando(marco_loading, "Iniciando sesión...")
        ventana.update()
        time.sleep(1)

    usuario, error = controlador.login(correo, contraseña)
    
    if usuario:
        if marco_loading:
            mostrar_cargando(marco_loading, "¡Bienvenido!\nCargando datos...")
            ventana.update()
            time.sleep(0.5)
        ir_a_pagina_principal(ventana, marco, usuario)
    else:
        if marco_loading:
             for widget in marco_loading.winfo_children(): widget.destroy()
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

