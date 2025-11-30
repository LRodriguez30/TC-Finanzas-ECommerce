import customtkinter as ctk
from frontend.ui.ecommerce.app import EcommerceApp
import customtkinter as ctk
from frontend.ui.ecommerce.app import EcommerceApp

def mostrar_pagina_principal(root, usuario):
    # Clear existing widgets in root (if any, though login usually clears itself or we might need to)
    for widget in root.winfo_children():
        widget.destroy()
        
    # Initialize the Ecommerce App
    app = EcommerceApp(root, usuario)
    
    # Resize window for the dashboard
    root.geometry("1200x800")
    root.minsize(1000, 600)
    root.maxsize(2000, 1500) # Or just remove maxsize constraint if possible, but CTk might need it reset
    root.resizable(True, True)