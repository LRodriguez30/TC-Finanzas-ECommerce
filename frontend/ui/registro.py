import customtkinter as ctk
from typing import Dict
from frontend.widgets.frames import Marco
from frontend.widgets.contained_elements import Elementos
from frontend.components.events import registrar
from frontend.components.navigation import ir_a_login

def mostrar_registro(ventana_principal: ctk.CTk) -> None:
    """
    Muestra la interfaz de registro de usuario en la ventana principal.
    """

    # Limitar tamaño de ventana
    ventana_principal.minsize(800, 650)
    ventana_principal.maxsize(800, 650)

    # Marco principal
    marco_principal: Marco = Marco(
        ventana_principal=ventana_principal,
        radio_esquinas=0,
        color_fondo="#ffffff",
        ancho_relativo=1,
        alto_relativo=1
    )

    # Sub-marco formulario (50%)
    marco_formulario: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=10,
        color_fondo="#ffffff",
        ancho_relativo=0.5,
        alto_relativo=1
    )

    # Sub-marco derecho: fondo naranja (50%)
    marco_derecho: Marco = Marco(
        ventana_principal=marco_principal,
        radio_esquinas=0,
        color_fondo="#FFA500",
        ancho_relativo=0.5,
        alto_relativo=1
    )
    marco_derecho.place(relx=0.5, rely=0)

    # Acceder a los elementos del formulario
    elementos: Elementos = marco_formulario.elementos

    # Título
    elementos.EtiquetaDeTexto(
        "Registro de Usuario",
        tamaño_fuente=20,
        peso="bold",
        margen=(20, 10)
    )

    # Selección de rol
    combo_rol: ctk.CTkComboBox = ctk.CTkComboBox(
        marco_formulario,
        values=["Administrador", "Vendedor", "Comprador"]
    )
    combo_rol.pack(pady=5, padx=20, fill="x")

    # Entradas de texto
    entrada_primer_nombre: ctk.CTkEntry = elementos.CampoDeTexto("Primer Nombre")
    entrada_segundo_nombre: ctk.CTkEntry = elementos.CampoDeTexto("Segundo Nombre")
    entrada_primer_apellido: ctk.CTkEntry = elementos.CampoDeTexto("Primer Apellido")
    entrada_segundo_apellido: ctk.CTkEntry = elementos.CampoDeTexto("Segundo Apellido")
    entrada_telefono: ctk.CTkEntry = elementos.CampoDeTexto("Teléfono")
    entrada_correo: ctk.CTkEntry = elementos.CampoDeTexto("Correo")
    entrada_contraseña: ctk.CTkEntry = elementos.CampoDeTexto("Contraseña", show="*")
    entrada_confirmar_contraseña: ctk.CTkEntry = elementos.CampoDeTexto("Confirmar Contraseña", show="*")

    # Etiqueta para mostrar mensajes
    etiqueta_mensaje: ctk.CTkLabel = elementos.EtiquetaDeTexto(
        "",
        color="green",
        margen=(5, 5)
    )

    # Limpiar mensaje al escribir en cualquier campo
    for campo in [entrada_primer_nombre, entrada_segundo_nombre,
                  entrada_primer_apellido, entrada_segundo_apellido,
                  entrada_telefono, entrada_correo, entrada_contraseña,
                  entrada_confirmar_contraseña]:
        campo.bind("<Key>", lambda e: etiqueta_mensaje.configure(text=""))

    # Botón para registrar usuario
    elementos.Boton(
        "Registrar",
        lambda: registrar(
            {
                "id_rol": {"Administrador": 1, "Vendedor": 2, "Comprador": 3}.get(combo_rol.get(), 3),
                "primer_nombre": entrada_primer_nombre.get(),
                "segundo_nombre": entrada_segundo_nombre.get(),
                "primer_apellido": entrada_primer_apellido.get(),
                "segundo_apellido": entrada_segundo_apellido.get(),
                "telefono": entrada_telefono.get(),
                "correo": entrada_correo.get(),
                "contraseña": entrada_contraseña.get(),
                "confirmar_contraseña": entrada_confirmar_contraseña.get()
            },
            etiqueta_mensaje,
            ventana_principal,
            marco_principal
        )
    )

    # Link para ir al login
    elementos.Enlace(
        "¿Ya tienes una cuenta? Inicia sesión aquí",
        lambda: ir_a_login(ventana_principal, marco_principal)
    )