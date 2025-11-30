# contained_elements.py
from .elements import crear_boton, crear_campo_de_texto, crear_etiqueta_de_texto, crear_enlace
import customtkinter as ctk
from typing import Optional, Tuple, Callable

class Elementos:
    def __init__(self, ventana: ctk.CTkFrame) -> None:
        self.contenedor: ctk.CTkFrame = ventana

    def CampoDeTexto(self, placeholder: str, show: Optional[str] = None) -> ctk.CTkEntry:
        return crear_campo_de_texto(self.contenedor, placeholder, show)

    def Boton(
        self,
        texto: str,
        accion: Callable[[], None],
        ancho: int = 200,
        margen_sup: int = 10,
        margen_inf: int = 10
    ) -> ctk.CTkButton:
        return crear_boton(self.contenedor, texto, accion, ancho, margen_sup, margen_inf)

    def EtiquetaDeTexto(
        self,
        texto: str,
        tamaño_fuente: int = 14,
        peso: Optional[str] = None,
        color: str = "black",
        margen: Tuple[int, int] = (0, 0)
    ) -> ctk.CTkLabel:
        return crear_etiqueta_de_texto(self.contenedor, texto, tamaño_fuente, peso, color, margen)

    def Enlace(
        self,
        texto: str,
        accion: Callable[[], None],
        color_normal: str = "blue",
        color_hover: str = "#1E90FF",
        tamaño_fuente: int = 12,
        margen_sup: int = 10,
        margen_inf: int = 20
    ) -> ctk.CTkLabel:
        return crear_enlace(
            self.contenedor,
            texto,
            accion,
            color_normal,
            color_hover,
            tamaño_fuente,
            margen_sup,
            margen_inf
        )