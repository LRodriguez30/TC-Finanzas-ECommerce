import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, logout_callback=None):
        # Por defecto usa una paleta verde oliva; puede actualizarse mediante `apply_palette`
        super().__init__(master, width=250, corner_radius=0, fg_color="#65A30D") # Olive Green
        self.navigate_callback = navigate_callback
        self.logout_callback = logout_callback
        
        # Configure grid layout
        self.grid_rowconfigure(6, weight=1) # Spacer
        
        # Header
        self.logo_label = ctk.CTkLabel(self, text="LRR\nEcommerce\nSYSTEM", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation Buttons
        self.home_button = self.create_nav_button("Inicio", "HOME", 1)
        self.products_button = self.create_nav_button("Productos", "PRODUCTS", 2)
        self.sellers_button = self.create_nav_button("Vendedores", "SELLERS", 3)
        self.financial_button = self.create_nav_button("Análisis Financiero", "FINANCIAL", 4)
        self.account_button = self.create_nav_button("Mi Cuenta", "ACCOUNT", 5)
        
        # Logout Button
        self.logout_button = ctk.CTkButton(self, text="Cerrar Sesión", fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#D97706", anchor="w", command=self._on_logout_pressed)
        self.logout_button.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
    def create_nav_button(self, text, view_name, row):
        button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=text,
                                fg_color="transparent", text_color="white", hover_color="#F97316", # Orange Hover
                                anchor="w", command=lambda: self.navigate_callback(view_name))
        button.grid(row=row, column=0, sticky="ew")
        return button

    def apply_palette(self, palette: dict):
        """
        Aplica una paleta visual al sidebar: actualiza color de fondo y colores de hover/borde.
        Espera un dict con claves: 'sidebar_bg', 'accent', 'hover'.
        """
        try:
            sidebar_bg = palette.get('sidebar_bg', '#65A30D')
            hover = palette.get('hover', '#F97316')
            accent = palette.get('accent', '#F97316')

            self.configure(fg_color=sidebar_bg)

            # Actualizar botones de navegación
            for btn in [self.home_button, self.products_button, self.sellers_button, self.financial_button, self.account_button]:
                try:
                    btn.configure(hover_color=hover)
                except Exception:
                    pass

            # Logout button: usar borde y hover acorde a la paleta
            try:
                self.logout_button.configure(border_color='white' if self._is_contrast_light(sidebar_bg) else 'black', hover_color=hover)
            except Exception:
                pass
        except Exception as e:
            print("Error applying palette to sidebar:", e)

    def _is_contrast_light(self, hexcolor: str) -> bool:
        """Retorna True si el color hexadecimal es claro (para elegir color de borde apropiado)."""
        hexcolor = hexcolor.lstrip('#')
        try:
            r, g, b = int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
            luminance = (0.2126*r + 0.7152*g + 0.0722*b)
            return luminance > 128
        except Exception:
            return True

    def _on_logout_pressed(self):
        """
        Llamado cuando se presiona el botón de cerrar sesión.
        Si se proporcionó un callback (por ejemplo `EcommerceApp.logout_event`), lo ejecuta;
        en caso contrario imprime un mensaje (modo fallback para pruebas).
        """
        if callable(self.logout_callback):
            try:
                self.logout_callback()
            except Exception as e:
                print("Error al ejecutar logout_callback:", e)
        else:
            print("Logout pressed")
