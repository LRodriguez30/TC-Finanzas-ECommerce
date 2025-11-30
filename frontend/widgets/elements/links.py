import customtkinter as ctk
from typing import Callable

def crear_enlace(
    ventana: ctk.CTkFrame,
    texto: str,
    accion: Callable[[], None],
    color_normal: str = "blue",
    color_al_señalar: str = "#1E90FF",
    tamaño_fuente: int = 12,
    margen_superior: int = 10,
    margen_inferior: int = 20
) -> ctk.CTkLabel:
    """
    Crea un enlace (link) con estilo uniforme para un ventana.

    Parámetros:
    - ventana: CTkFrame donde se añadirá el link
    - texto: str, texto que se mostrará en el link
    - accion: función que se ejecutará al hacer clic en el link
    - color_normal: str, color del texto por defecto (por defecto "blue")
    - color_al_señalar: str, color del texto al pasar el mouse (por defecto "#1E90FF")
    - tamaño_fuente: int, tamaño de la letra (por defecto 12)
    - margen_superior: int, espacio en píxeles sobre el link (por defecto 10)
    - margen_inferior: int, espacio en píxeles debajo del link (por defecto 20)

    Retorna:
    - ctk.CTkLabel: el link creado
    """
    enlace = ctk.CTkLabel(
        ventana,
        text=texto,
        text_color=color_normal,
        fg_color="transparent",
        font=ctk.CTkFont(size=tamaño_fuente, underline=True)
    )
    enlace.pack(pady=(margen_superior, margen_inferior))

    # Cambiar color al pasar el mouse
    enlace.bind("<Enter>", lambda _: enlace.configure(text_color=color_al_señalar))
    enlace.bind("<Leave>", lambda _: enlace.configure(text_color=color_normal))

    # Ejecutar acción al hacer clic
    enlace.bind("<Button-1>", lambda _: accion())

    return enlace
