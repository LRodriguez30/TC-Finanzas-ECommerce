from customtkinter import CTkFrame, CTk

def ir_a_login(ventana: CTk, marco: CTkFrame):
    """
    Destruye el marco actual y muestra la pantalla de login.
    
    Parámetros:
    - ventana: ventana principal donde se cargará la nueva pantalla
    - marco: marco que se destruirá antes de mostrar el login
    """
    marco.destroy()

    from frontend.ui.login import mostrar_login
    mostrar_login(ventana)

def ir_a_registro(ventana: CTk, marco: CTkFrame):
    """
    Destruye el frame actual y muestra la pantalla de registro.
    
    Parámetros:
    - ventana: ventana principal donde se cargará la nueva pantalla
    - marco: marco que se destruirá antes de mostrar el registro
    """
    marco.destroy()

    from frontend.ui.registro import mostrar_registro
    mostrar_registro(ventana)

def ir_a_pagina_principal(ventana: CTk, marco: CTkFrame, usuario):
    """
    Destruye el frame actual y muestra la página principal del usuario.
    
    Parámetros:
    - ventana: ventana principal donde se cargará la página
    - marco: marco que se destruirá antes de mostrar la página principal
    - usuario: objeto con información del usuario logueado
    """
    marco.destroy()
    from frontend.ui.pagina_principal import mostrar_pagina_principal
    mostrar_pagina_principal(ventana, usuario)

def cerrar_sesion(root, frame):
    frame.destroy()     # Elimina la vista principal
    from frontend.ui.login import mostrar_login
    mostrar_login(root) # Vuelve al login