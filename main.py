import customtkinter as ctk
from frontend.ui.login import mostrar_login

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("ECommerce - Login")

    # Tamaño de la ventana
    root_width = 400
    root_height = 500

    # Obtener tamaño de pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular coordenadas para centrar la ventana
    x = (screen_width - root_width) // 2
    y = (screen_height - root_height) // 2

    # Establecer tamaño y posición
    root.geometry(f"{root_width}x{root_height}+{x}+{y}")

    mostrar_login(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()