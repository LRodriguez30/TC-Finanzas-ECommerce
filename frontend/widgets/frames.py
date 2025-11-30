import customtkinter as ctk
from typing import Optional, Union
from .contained_elements import Elementos

class Marco(ctk.CTkFrame):
    """
    Contenedor principal de la interfaz con opciones de padding, tamaño relativo,
    y acceso a widgets internos a través de `elementos`.

    Parámetros:
    - contenedor_padre: Contenedor donde se añadirá el marco (CTkFrame u otro Frame)
    - radio_esquinas: Radio de las esquinas del marco (por defecto 10)
    - color_fondo: Color de fondo del marco (por defecto "#ffffff")
    - margen_horizontal: Espacio horizontal alrededor del marco (por defecto 0)
    - margen_vertical: Espacio vertical alrededor del marco (por defecto 0)
    - ancho_relativo: Ancho relativo al contenedor padre (0.0 a 1.0)
    - alto_relativo: Alto relativo al contenedor padre (0.0 a 1.0)
    - kwargs: Argumentos adicionales que acepte CTkFrame
    """

    def __init__(
        self,
        ventana_principal: Union[ctk.CTk, ctk.CTkFrame],
        radio_esquinas: int = 10,
        color_fondo: str = "#ffffff",
        margen_horizontal: int = 0,
        margen_vertical: int = 0,
        ancho_relativo: Optional[float] = None,
        alto_relativo: Optional[float] = None,
        **kwargs
    ):
        super().__init__(ventana_principal, corner_radius=radio_esquinas, fg_color=color_fondo, **kwargs)

        # Geometry manager seguro: usar place si hay dimensiones relativas, si no, pack
        if ancho_relativo is not None or alto_relativo is not None:
            self.place(
                relx=0,
                rely=0,
                relwidth=ancho_relativo if ancho_relativo is not None else 1,
                relheight=alto_relativo if alto_relativo is not None else 1
            )
        else:
            self.pack(padx=margen_horizontal, pady=margen_vertical)

        # Instancia los elementos dentro del marco
        self.elementos: Elementos = Elementos(self)