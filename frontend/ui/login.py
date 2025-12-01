from frontend.widgets.frames import Marco
from frontend.components.events import iniciar_sesion
from frontend.components.navigation import ir_a_registro
import customtkinter as ctk
from frontend.widgets.contained_elements import Elementos

def mostrar_login(ventana_principal: ctk.CTk) -> None:
    """
    Muestra la interfaz de inicio de sesión en la ventana principal.
    """

    # Limitar tamaño mínimo y máximo de la ventana
    ventana_principal.minsize(800, 400)
    ventana_principal.maxsize(800, 400)

    # Marco principal que ocupa toda la ventana
    marco_principal: Marco = Marco(
        ventana_principal=ventana_principal,
        radio_esquinas=0,
        color_fondo="#ffffff",
        ancho_relativo=1,
        alto_relativo=1
    )

    # Sub-marco izquierdo: formulario de login (40%)
    marco_izquierdo: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=0,
        color_fondo="#ffffff",
        ancho_relativo=0.4,
        alto_relativo=1
    )

    # Sub-marco derecho: fondo naranja (60%)
    marco_derecho: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=0,
        color_fondo="#FFA500",
        ancho_relativo=0.6,
        alto_relativo=1
    )
    marco_derecho.place(relx=0.4, rely=0)

    # Acceder a los elementos del marco izquierdo
    elementos: Elementos = marco_izquierdo.elementos

    # Título
    elementos.EtiquetaDeTexto(
        "Iniciar Sesión",
        tamaño_fuente=20,
        peso="bold",
        margen=(50, 20)
    )

    # Etiqueta para mostrar mensajes de error
    etiqueta_mensaje: ctk.CTkLabel = elementos.EtiquetaDeTexto(
        "",
        color="red",
        margen=(5, 5)
    )

    # Campos de texto
    entrada_correo: ctk.CTkEntry = elementos.CampoDeTexto("Correo")
from frontend.widgets.frames import Marco
from frontend.components.events import iniciar_sesion
from frontend.components.navigation import ir_a_registro
import customtkinter as ctk
from frontend.widgets.contained_elements import Elementos

def mostrar_login(ventana_principal: ctk.CTk) -> None:
    """
    Muestra la interfaz de inicio de sesión en la ventana principal.
    """

    # Limitar tamaño mínimo y máximo de la ventana
    ventana_principal.minsize(800, 400)
    ventana_principal.maxsize(800, 400)

    # Marco principal que ocupa toda la ventana
    marco_principal: Marco = Marco(
        ventana_principal=ventana_principal,
        radio_esquinas=0,
        color_fondo="#ffffff",
        ancho_relativo=1,
        alto_relativo=1
    )

    # Sub-marco izquierdo: formulario de login (40%)
    marco_izquierdo: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=0,
        color_fondo="#ffffff",
        ancho_relativo=0.4,
        alto_relativo=1
    )

    # Sub-marco derecho: fondo naranja (60%)
    marco_derecho: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=0,
        color_fondo="#FFA500",
        ancho_relativo=0.6,
        alto_relativo=1
    )
    marco_derecho.place(relx=0.4, rely=0)

    # Acceder a los elementos del marco izquierdo
    elementos: Elementos = marco_izquierdo.elementos

    # Título
    elementos.EtiquetaDeTexto(
        "Iniciar Sesión",
        tamaño_fuente=20,
        peso="bold",
        margen=(50, 20)
    )

    # Etiqueta para mostrar mensajes de error
    etiqueta_mensaje: ctk.CTkLabel = elementos.EtiquetaDeTexto(
        "",
        color="red",
        margen=(5, 5)
    )

    # Campos de texto
    entrada_correo: ctk.CTkEntry = elementos.CampoDeTexto("Correo")
    entrada_contraseña: ctk.CTkEntry = elementos.CampoDeTexto("Contraseña", show="*")

    # Limpiar mensaje al escribir en cualquier campo
    entrada_correo.bind("<Key>", lambda e: etiqueta_mensaje.configure(text=""))
    entrada_contraseña.bind("<Key>", lambda e: etiqueta_mensaje.configure(text=""))

    # Botón para iniciar sesión
    elementos.Boton(
        "Ingresar",
        lambda: iniciar_sesion(
            correo=entrada_correo.get(),
            contraseña=entrada_contraseña.get(),
            etiqueta_mensaje=etiqueta_mensaje,
            ventana=ventana_principal,
            marco=marco_principal,
            marco_loading=marco_derecho
        )
    )

    # Link para ir al registro
    elementos.Enlace(
        "¿No tienes una cuenta? Regístrate aquí",
        lambda: ir_a_registro(ventana_principal, marco_principal)
    )