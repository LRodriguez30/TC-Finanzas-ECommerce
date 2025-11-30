import customtkinter as ctk
from .sidebar import Sidebar
from .pages.home import HomePage
from .pages.products import ProductsPage
from .pages.financial import FinancialPage
from .pages.sellers import SellersPage

class EcommerceApp(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        # Configure grid layout for the main frame
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Pages
        self.pages = {}
        self.current_view = None
        
        # Initialize pages
        self.pages["HOME"] = HomePage(self.main_frame)
        self.pages["PRODUCTS"] = ProductsPage(self.main_frame)
        self.pages["FINANCIAL"] = FinancialPage(self.main_frame)
        self.pages["SELLERS"] = SellersPage(self.main_frame)
        self.pages["ACCOUNT"] = ctk.CTkLabel(self.main_frame, text=f"Cuenta de {usuario.primer_nombre if usuario else 'Usuario'}", font=ctk.CTkFont(size=20))

        # Start with Home
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
        # This should probably call a callback to return to login
        # For now, just print
        print("Logout requested")
        # In a real integration, we'd call a callback passed from main
