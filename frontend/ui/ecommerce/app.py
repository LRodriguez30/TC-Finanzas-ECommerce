import customtkinter as ctk
from .sidebar import Sidebar
from .pages.home import HomePage
from .pages.products import ProductsPage
from .pages.financial import FinancialPage
from .pages.account import AccountPage
from .pages.sellers import SellersPage
from .pages.financialEcommerce import FinancialEcommercePage
from .pages.financialVendedor import FinancialVendedorPage
from frontend.components.navigation import cerrar_sesion

class EcommerceApp(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.usuario = usuario
        
        # Configura la distribución de cuadrícula para el marco principal
        # (define cómo se expanden y comportan las filas/columnas cuando la ventana cambia de tamaño)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Barra lateral (navegación)
        # Contiene los elementos de navegación que permiten cambiar entre vistas/páginas
        user_role = self.usuario.id_rol if self.usuario else 0
        self.sidebar = Sidebar(self, self.navigate, logout_callback=self.logout_event, user_role=user_role)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Área principal de contenido
        # Aquí se montan las páginas dinámicas que muestran la UI principal (productos, finanzas, etc.)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Páginas (vistas)
        # Diccionario con instancias de las diferentes vistas que la app puede mostrar
        self.pages = {}
        self.current_view = None
        
        # Inicializa las páginas y componentes principales usados en la app
        self.pages["HOME"] = HomePage(self.main_frame)
        self.pages["PRODUCTS"] = ProductsPage(self.main_frame)
        self.pages["FINANCIAL"] = FinancialPage(self.main_frame)
        self.pages["SELLERS"] = SellersPage(self.main_frame)
        self.pages["ACCOUNT"] = AccountPage(self.main_frame, app_reference=self)
        self.pages["FINANCIALECOMMERCE"] = FinancialEcommercePage(self.main_frame)
        self.pages["FINANCIALVENDEDOR"] = FinancialVendedorPage(self.main_frame, usuario=self.usuario)

        # Paleta por defecto (puede ser cambiada desde la página 'Mi Cuenta')
        self.current_palette = {'sidebar_bg': '#65A30D', 'accent': '#65A30D', 'hover': '#F97316'}
        # Aplicar paleta inicial al sidebar
        try:
            self.sidebar.apply_palette(self.current_palette)
        except Exception:
            pass

        # Mostrar la vista 'HOME' por defecto al iniciar la aplicación
        self.navigate("HOME")

    def navigate(self, view_name):
        if self.current_view:
            self.current_view.pack_forget()
            
        if view_name in self.pages:
            self.current_view = self.pages[view_name]
            self.current_view.pack(fill="both", expand=True)
        else:
            print(f"View {view_name} not found")

    def logout_event(self):
        cerrar_sesion(self.master, self)

    def set_palette(self, palette: dict):
        """
        Aplica la paleta a los componentes principales de la app.
        """
        self.current_palette = palette
        # Aplicar al sidebar
        try:
            self.sidebar.apply_palette(palette)
        except Exception:
            pass

        # Aplicar color de fondo principal si se especifica
        try:
            main_bg = palette.get('main_bg', None)
            if main_bg is not None:
                self.main_frame.configure(fg_color=main_bg)
        except Exception:
            pass

        # Aplicar a otras páginas que implementen apply_palette
        for page in self.pages.values():
            if hasattr(page, 'apply_palette'):
                try:
                    page.apply_palette(palette)
                except Exception:
                    pass