import customtkinter as ctk
from ..theme_manager import available_palettes, set_palette, get_color


class AccountPage(ctk.CTkFrame):
    def __init__(self, master, app_reference=None):
        super().__init__(master, fg_color="transparent")
        self.app = app_reference

        header = ctk.CTkLabel(self, text="Mi Cuenta", font=ctk.CTkFont(size=20, weight='bold'), text_color=get_color('text'))
        header.pack(anchor='w', pady=(6,12), padx=8)

        # Paleta
        frame = ctk.CTkFrame(self, fg_color='transparent')
        frame.pack(fill='x', padx=8)

        ctk.CTkLabel(frame, text='Paleta de Colores:', text_color=get_color('text')).pack(side='left')
        self.palette_var = ctk.StringVar(value=available_palettes()[0])
        opt = ctk.CTkOptionMenu(frame, values=available_palettes(), variable=self.palette_var, width=180)
        opt.pack(side='left', padx=8)

        ctk.CTkButton(frame, text='Aplicar', command=self.apply_palette, fg_color=get_color('primary')).pack(side='left', padx=8)

        # Perfil simple
        prof = ctk.CTkFrame(self, fg_color=get_color('card_bg'))
        prof.pack(fill='x', padx=8, pady=12)
        ctk.CTkLabel(prof, text='Nombre:', text_color=get_color('text')).grid(row=0, column=0, sticky='w', padx=6, pady=6)
        ctk.CTkEntry(prof, placeholder_text='Tu nombre').grid(row=0, column=1, padx=6, pady=6)

        ctk.CTkLabel(prof, text='Correo:', text_color=get_color('text')).grid(row=1, column=0, sticky='w', padx=6, pady=6)
        ctk.CTkEntry(prof, placeholder_text='tu@correo.com').grid(row=1, column=1, padx=6, pady=6)

    def apply_palette(self):
        chosen = self.palette_var.get()
        ok = set_palette(chosen)
        if ok and self.app:
            # Notify app pages to refresh theme if they implement on_theme_change
            for p in self.app.pages.values():
                if hasattr(p, 'on_theme_change'):
                    try:
                        p.on_theme_change()
                    except Exception:
                        pass
            # Also refresh current view
            if hasattr(self.app, 'navigate'):
                self.app.navigate('ACCOUNT')
