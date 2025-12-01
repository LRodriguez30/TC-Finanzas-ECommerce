import customtkinter as ctk

def mostrar_cargando(frame: ctk.CTkFrame, mensaje: str = "Cargando..."):
    """
    Muestra una animación de carga en el frame proporcionado.
    Limpia el contenido actual del frame antes de mostrar la carga.
    """
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Configurar grid para centrar contenido
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=1)

    # Contenedor para centrar
    contenedor = ctk.CTkFrame(frame, fg_color="transparent")
    contenedor.grid(row=1, column=0)

    # Spinner / Barra de progreso
    # Usamos una barra de progreso indeterminada para simular carga
    progress = ctk.CTkProgressBar(contenedor, orientation="horizontal", mode="indeterminate", width=200)
    progress.pack(pady=(0, 15))
    progress.start()

    # Etiqueta de texto
    label = ctk.CTkLabel(contenedor, text=mensaje, font=("Arial", 16, "bold"), text_color="white")
    label.pack()

    # Forzar actualización de la UI
    frame.update_idletasks()
