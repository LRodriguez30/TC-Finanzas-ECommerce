import customtkinter as ctk
from typing import Callable

def crear_boton(
    marco: ctk.CTkFrame, 
    texto: str, 
    accion: Callable[[], None], 
    ancho: int = 200, 
    margen_superior: int = 10, 
    margen_inferior: int = 10
) -> ctk.CTkButton:
    """
    Crea un botón con estilo uniforme para un formulario.

    Parámetros:
    - marco: CTkFrame donde se añadirá el botón
    - texto: str, texto que se mostrará en el botón
    - accion: función que se ejecutará al hacer clic en el botón
    - ancho: int, ancho del botón en píxeles (por defecto 200)
    - margen_superior: int, espacio en píxeles por encima del botón (por defecto 10)
    - margen_inferior: int, espacio en píxeles por debajo del botón (por defecto 10)

    Retorna:
    - ctk.CTkButton: el botón creado
    """
    boton = ctk.CTkButton(marco, text=texto, command=accion, width=ancho)
    boton.pack(pady=(margen_superior, margen_inferior))
    return boton