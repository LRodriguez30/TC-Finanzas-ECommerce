import customtkinter as ctk
from typing import Optional

def crear_campo_de_texto(
    marco: ctk.CTkFrame,
    texto_ejemplo: str,
    ocultar: Optional[str] = None,
    padding_vertical: int = 10,
    padding_horizontal: int = 20
) -> ctk.CTkEntry:
    """
    Crea un campo de texto (CTkEntry) con estilo y padding uniforme.

    Parámetros:
    - marco: contenedor donde se añadirá el campo (CTkFrame o similar)
    - texto_ejemplo: texto que se mostrará como placeholder
    - ocultar: caracter para ocultar la entrada (por ejemplo '*'), opcional
    - padding_vertical: espacio en píxeles arriba y abajo del campo (por defecto 10)
    - padding_horizontal: espacio en píxeles a los lados del campo (por defecto 20)

    Retorna:
    - El campo de texto creado (CTkEntry)
    """
    campo = ctk.CTkEntry(marco, placeholder_text=texto_ejemplo, show=ocultar)
    campo.pack(pady=padding_vertical, padx=padding_horizontal, fill="x")
    return campo