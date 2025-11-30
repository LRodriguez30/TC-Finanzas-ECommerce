import customtkinter as ctk
from typing import Tuple, Optional

def crear_etiqueta_de_texto(
    marco: ctk.CTkFrame,
    texto: str,
    tamaño_fuente: int = 14,
    peso: Optional[str] = None,
    color: str = "black",
    margen: Tuple[int, int] = (0, 0),
    font: Optional[ctk.CTkFont] = None
) -> ctk.CTkLabel:
    """
    Crea un label (etiqueta) con estilo uniforme para un marco.

    Parámetros:
    - marco: CTkFrame donde se añadirá el label
    - texto: str, texto que se mostrará en el label
    - tamaño_fuente: int, tamaño de la letra (por defecto 14)
    - peso: str | None, "normal" o "bold" para negrita (solo usado si font no se pasa)
    - color: str, color del texto (por defecto "black")
    - margen: tuple(int, int), espacio superior e inferior en píxeles (por defecto (0,0))
    - font: ctk.CTkFont | None, si se pasa, se usa directamente este objeto

    Retorna:
    - ctk.CTkLabel: el label creado
    """
    # Si no se pasa font, crear uno con tamaño y peso
    if font is None:
        if peso in ("normal", "bold"):
            font = ctk.CTkFont(size=tamaño_fuente, weight=peso)
        else:
            font = ctk.CTkFont(size=tamaño_fuente)

    label = ctk.CTkLabel(marco, text=texto, font=font, text_color=color)
    label.pack(pady=margen)
    return label