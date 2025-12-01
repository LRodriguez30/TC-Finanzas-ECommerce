import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Título principal
        self.label = ctk.CTkLabel(self, text="Bienvenido al Sistema LRR Ecommerce", font=ctk.CTkFont(size=28, weight="bold"), text_color="#111827")
        self.label.pack(pady=(40, 20), padx=20)
        
        # Contenedor de bienvenida
        welcome_frame = ctk.CTkFrame(self, fg_color="#F3F4F6", corner_radius=10)
        welcome_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Mensaje de bienvenida
        welcome_text = """
🛒 Plataforma Integral de Comercio Electrónico

Bienvenido a tu solución completa para gestionar tu negocio en línea. 
Nuestra plataforma te ofrece:

✨ Compra y Venta de Productos
   • Explora un amplio catálogo de productos
   • Publica y gestiona tus propios productos como vendedor
   • Realiza transacciones seguras y confiables

📊 Análisis Financiero Personal
   • Gestiona las finanzas de tu negocio
   • Visualiza estados financieros en tiempo real
   • Genera reportes detallados de tus operaciones

👥 Gestión de Vendedores
   • Administra tu perfil de vendedor
   • Controla tu inventario y ventas
   • Accede a herramientas especializadas para tu negocio

💼 Panel de Control Personalizado
   • Interfaz intuitiva y fácil de usar
   • Acceso rápido a todas las funcionalidades
   • Experiencia adaptada a tu rol (Comprador, Vendedor o Administrador)

Selecciona una opción del menú lateral para comenzar tu experiencia.
        """
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text=welcome_text.strip(),
            font=ctk.CTkFont(size=14),
            text_color="#374151",
            justify="left"
        )
        welcome_label.pack(pady=30, padx=30)
