import customtkinter as ctk

def mostrar_pagina_principal(root, usuario):
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text=f"Bienvenido {usuario.primer_nombre}").pack()
    ctk.CTkLabel(frame, text=f"Rol: {usuario.id_rol}").pack()