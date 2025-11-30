import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.label = ctk.CTkLabel(self, text="Bienvenido al Sistema LRR Ecommerce", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=40, padx=20)
        
        self.info_label = ctk.CTkLabel(self, text="Seleccione una opción del menú lateral para comenzar.", font=ctk.CTkFont(size=16))
        self.info_label.pack(pady=10)
