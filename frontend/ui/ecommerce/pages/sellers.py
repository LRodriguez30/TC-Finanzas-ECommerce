import customtkinter as ctk
from tkinter import filedialog

class SellersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Main Card Container with Border
        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=1, border_color="gray50")
        self.card.pack(fill="both", expand=True, padx=40, pady=20)
        
        # --- Header (Orange) ---
        self.header = ctk.CTkFrame(self.card, fg_color="#F97316", corner_radius=10, height=60) # Orange color
        self.header.pack(fill="x", padx=2, pady=2) # Small padding to show border
        
        self.title = ctk.CTkLabel(self.header, text="Registro para Vendedores", 
                                  font=ctk.CTkFont(family="Serif", size=24, weight="bold", slant="italic"),
                                  text_color="black")
        self.title.place(relx=0.5, rely=0.5, anchor="center")
        
        # --- Form Content ---
        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Title "Registro"
        self.lbl_registro = ctk.CTkLabel(self.form_frame, text="Registro", text_color="green", 
                                         font=ctk.CTkFont(size=16))
        self.lbl_registro.pack(anchor="w")
        
        # Separator line
        self.line = ctk.CTkProgressBar(self.form_frame, height=1, progress_color="green")
        self.line.set(1)
        self.line.pack(fill="x", pady=(0, 20))

        # 1. Business Name
        self.add_question("¿Cual sera el nombre de tu negocio?")
        self.entry_name = ctk.CTkEntry(self.form_frame, height=40, fg_color="#D1D5DB", border_width=0, text_color="black") # Gray background
        self.entry_name.pack(fill="x", pady=(0, 15))
        
        # 2. Logo Upload
        self.add_question("¿Cual sera tu logo?")
        self.logo_frame = ctk.CTkFrame(self.form_frame, fg_color="white", border_width=1, border_color="#F97316", height=100)
        self.logo_frame.pack(fill="x", pady=(0, 15))
        self.logo_frame.pack_propagate(False)
        
        self.btn_upload = ctk.CTkButton(self.logo_frame, text="arrastra tu logo aqui\nclick para subir logo", 
                                        fg_color="transparent", text_color="black", hover=False,
                                        command=self.upload_logo)
        self.btn_upload.place(relx=0.5, rely=0.5, anchor="center")
        
        # 3. Description
        self.add_question("¿Cual sera la descripcion de tu negocio?")
        self.txt_desc = ctk.CTkTextbox(self.form_frame, height=100, fg_color="#D1D5DB", text_color="black", border_width=0)
        self.txt_desc.pack(fill="x", pady=(0, 5))
        self.txt_desc.bind("<KeyRelease>", self.update_word_count)
        
        self.lbl_count = ctk.CTkLabel(self.form_frame, text="Palabras escritas : 0 / 0", text_color="#854D0E") # Brownish
        self.lbl_count.pack(anchor="e", pady=(0, 15))
        
        # 4. DGI
        self.add_question("Tu negocio esta registrado en la DGI?")
        self.dgi_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.dgi_frame.pack(anchor="w", pady=(0, 20))
        
        self.dgi_var = ctk.StringVar(value="No")
        self.btn_si = ctk.CTkButton(self.dgi_frame, text="Si", width=60, fg_color="white", text_color="black", border_width=1, border_color="black", hover_color="#EEE", command=lambda: self.dgi_var.set("Si"))
        self.btn_si.pack(side="left", padx=(0, 10))
        self.btn_no = ctk.CTkButton(self.dgi_frame, text="No", width=60, fg_color="white", text_color="black", border_width=1, border_color="black", hover_color="#EEE", command=lambda: self.dgi_var.set("No"))
        self.btn_no.pack(side="left")
        
        # --- Action Buttons ---
        self.actions_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=20)
        
        self.btn_register = ctk.CTkButton(self.actions_frame, text="Registrarte", fg_color="#D97706", # Darker Orange
                                          font=ctk.CTkFont(weight="bold", size=16), height=40,
                                          command=self.register)
        self.btn_register.pack(side="left", expand=True, padx=5)
        
        self.btn_cancel = ctk.CTkButton(self.actions_frame, text="Cancelar", fg_color="#65A30D", # Olive Green
                                        font=ctk.CTkFont(weight="bold", size=16), height=40,
                                        command=lambda: print("Cancelled"))
        self.btn_cancel.pack(side="left", expand=True, padx=5)

    def add_question(self, text):
        label = ctk.CTkLabel(self.form_frame, text=text, font=ctk.CTkFont(size=14), text_color="black")
        label.pack(anchor="w", pady=(0, 5))

    def update_word_count(self, event):
        text = self.txt_desc.get("1.0", "end-1c")
        words = len(text.split())
        chars = len(text)
        self.lbl_count.configure(text=f"Palabras escritas : {words} / {chars}")

    def register(self):
        import json
        from tkinter import messagebox
        
        data = {
            "negocio": self.entry_name.get(),
            "logo_path": getattr(self, "logo_path", ""),
            "descripcion": self.txt_desc.get("1.0", "end-1c"),
            "dgi": self.dgi_var.get()
        }
        
        # Simple validation
        if not data["negocio"]:
            messagebox.showwarning("Datos Incompletos", "Por favor ingrese el nombre del negocio.")
            return

        try:
            # Append to a list in sellers.json
            try:
                with open("sellers.json", "r") as f:
                    sellers = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                sellers = []
                
            sellers.append(data)
            
            with open("sellers.json", "w") as f:
                json.dump(sellers, f, indent=2)
                
            messagebox.showinfo("Éxito", "Vendedor registrado correctamente.")
            
            # Clear form
            self.entry_name.delete(0, "end")
            self.txt_desc.delete("1.0", "end")
            self.dgi_var.set("No")
            self.lbl_count.configure(text="Palabras escritas : 0 / 0")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def upload_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if path:
            self.logo_path = path
            # Update button text or show icon to indicate selection
            self.btn_upload.configure(text=f"Logo seleccionado:\n{path.split('/')[-1]}")
