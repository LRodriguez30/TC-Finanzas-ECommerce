import customtkinter as ctk
from backend.services.usuariosService import UsuarioService

class AccountPage(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="transparent")
        self.usuario = usuario
        self.usuario_service = UsuarioService()

        # Cabecera
        header = ctk.CTkLabel(self, text="Mi Cuenta", font=ctk.CTkFont(size=20, weight="bold"))
        header.pack(anchor="nw", pady=(10, 20), padx=10)

        # Paleta de colores
        pal_frame = ctk.CTkFrame(self, fg_color="transparent")
        pal_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(pal_frame, text="Paleta de colores:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        btns = ctk.CTkFrame(pal_frame, fg_color="transparent")
        btns.pack(anchor="w", pady=8)

        # Tres opciones de paleta
        ctk.CTkButton(btns, text="Verde (predeterminado)", fg_color="#65A30D", hover_color="#5A9A22", command=lambda: self.apply_palette('verde')).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Naranja", fg_color="#F97316", hover_color="#D97706", command=lambda: self.apply_palette('naranja')).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Azul", fg_color="#1E40AF", hover_color="#1E3A8A", command=lambda: self.apply_palette('azul')).pack(side="left", padx=6)

        # Formulario para cambiar correo
        email_frame = ctk.CTkFrame(self, fg_color="#F3F4F6")
        email_frame.pack(fill="x", padx=10, pady=(15, 5))
        ctk.CTkLabel(email_frame, text="Cambiar correo electrónico:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.new_email_var = ctk.StringVar()
        ctk.CTkEntry(email_frame, placeholder_text="Nuevo correo", textvariable=self.new_email_var).pack(fill="x", padx=10, pady=6)
        self.email_msg = ctk.CTkLabel(email_frame, text="", text_color="red")
        self.email_msg.pack(anchor="w", padx=10)
        ctk.CTkButton(email_frame, text="Actualizar correo", command=self.update_email, fg_color="#065F46").pack(padx=10, pady=10, anchor="e")

        # Formulario para cambiar contraseña
        pwd_frame = ctk.CTkFrame(self, fg_color="#F3F4F6")
        pwd_frame.pack(fill="x", padx=10, pady=(5, 10))
        ctk.CTkLabel(pwd_frame, text="Cambiar contraseña:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.current_pwd = ctk.StringVar()
        self.new_pwd = ctk.StringVar()
        self.confirm_pwd = ctk.StringVar()

        ctk.CTkEntry(pwd_frame, placeholder_text="Contraseña actual", textvariable=self.current_pwd, show="*").pack(fill="x", padx=10, pady=4)
        ctk.CTkEntry(pwd_frame, placeholder_text="Nueva contraseña", textvariable=self.new_pwd, show="*").pack(fill="x", padx=10, pady=4)
        ctk.CTkEntry(pwd_frame, placeholder_text="Confirmar nueva contraseña", textvariable=self.confirm_pwd, show="*").pack(fill="x", padx=10, pady=4)

        self.pwd_msg = ctk.CTkLabel(pwd_frame, text="", text_color="red")
        self.pwd_msg.pack(anchor="w", padx=10)
        ctk.CTkButton(pwd_frame, text="Cambiar contraseña", command=self.update_password, fg_color="#065F46").pack(padx=10, pady=10, anchor="e")

    def apply_palette(self, name: str):
        """Solicita a la app que aplique la paleta seleccionada."""
        mapping = {
            'verde': {'sidebar_bg': '#65A30D', 'accent': '#65A30D', 'hover': '#5A9A22'},
            'naranja': {'sidebar_bg': '#F97316', 'accent': '#F97316', 'hover': '#D97706'},
            'azul': {'sidebar_bg': '#1E40AF', 'accent': '#1E40AF', 'hover': '#1E3A8A'}
        }
        palette = mapping.get(name, mapping['verde'])
        # El frame principal (master.master) es EcommerceApp (dependiendo de la jerarquía)
        try:
            app = self.master.master
            if hasattr(app, 'set_palette'):
                app.set_palette(palette)
        except Exception as e:
            print("No se pudo aplicar la paleta:", e)

    def update_email(self):
        nuevo = self.new_email_var.get().strip()
        if not nuevo:
            self.email_msg.configure(text="Ingrese un correo válido.")
            return

        if not self.usuario or not getattr(self.usuario, 'id', None):
            self.email_msg.configure(text="Usuario no identificado.")
            return

        res = self.usuario_service.cambiar_correo(self.usuario.id, nuevo)
        if res.get('exito'):
            self.email_msg.configure(text="Correo actualizado.", text_color="green")
        else:
            msg = res.get('mensajes', {}).get('general', 'Error al actualizar correo')
            self.email_msg.configure(text=msg, text_color="red")

    def update_password(self):
        actual = self.current_pwd.get()
        nueva = self.new_pwd.get()
        confirm = self.confirm_pwd.get()

        if nueva != confirm:
            self.pwd_msg.configure(text="Las contraseñas no coinciden.")
            return

        if not self.usuario or not getattr(self.usuario, 'id', None):
            self.pwd_msg.configure(text="Usuario no identificado.")
            return

        res = self.usuario_service.cambiar_contraseña(self.usuario.id, actual, nueva)
        if res.get('exito'):
            self.pwd_msg.configure(text="Contraseña actualizada.", text_color="green")
        else:
            msg = res.get('mensajes', {}).get('general', 'Error al cambiar contraseña')
            self.pwd_msg.configure(text=msg, text_color="red")
