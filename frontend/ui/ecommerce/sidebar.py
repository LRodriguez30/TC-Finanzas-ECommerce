import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, width=250, corner_radius=0, fg_color="#65A30D") # Olive Green
        self.navigate_callback = navigate_callback
        
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
        self.logout_button = ctk.CTkButton(self, text="Cerrar Sesión", fg_color="transparent", border_width=1, border_color="white", text_color="white", hover_color="#D97706", anchor="w", command=self.logout_event)
        self.logout_button.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
    def create_nav_button(self, text, view_name, row):
        button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text=text,
                               fg_color="transparent", text_color="white", hover_color="#F97316", # Orange Hover
                               anchor="w", command=lambda: self.navigate_callback(view_name))
        button.grid(row=row, column=0, sticky="ew")
        return button

    def logout_event(self):
        print("Logout pressed")
