import customtkinter as ctk
from frontend.ui.ecommerce.data import MOCK_PRODUCTS


class ProductsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Diseño: barra lateral izquierda para filtros y área de contenido a la derecha
        # (la barra lateral contiene controles de filtrado y la sección derecha muestra la rejilla de productos)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Panel de filtros (barra lateral) ---
        # Contiene búsqueda, rango de precio y otros filtros para refinar la lista de productos
        self.filters_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.filters_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        self.filter_label = ctk.CTkLabel(self.filters_frame, text="Filtros", font=ctk.CTkFont(size=18, weight="bold"))
        self.filter_label.pack(pady=20, padx=10, anchor="w")
        
        # Label "Buscar" debajo de "Filtros"
        self.buscar_label = ctk.CTkLabel(
        self.filters_frame,
        text="Buscar",
        font=ctk.CTkFont(size=15, weight="bold"),
        text_color="#374151"
        )
        self.buscar_label.pack(pady=(0, 0), padx=10, anchor="w")

        # Búsqueda
        # Campo que filtra los productos en tiempo real según el texto ingresado
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.update_products)
        self.search_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="Buscar...", textvariable=self.search_var)
        self.search_entry.pack(pady=10, padx=10, fill="x")
        
        # Rango de precio
        # Control deslizante para limitar el precio máximo mostrado en la rejilla
        self.price_label = ctk.CTkLabel(self.filters_frame, text="Precio Máximo: $1500", text_color="#854D0E")
        self.price_label.pack(pady=(20, 5), padx=10, anchor="w")
        
        self.price_slider = ctk.CTkSlider(self.filters_frame, from_=0, to=1500, command=self.update_price_label, button_color="#F97316", progress_color="#F97316")
        self.price_slider.set(1000)
        self.price_slider.pack(pady=5, padx=10, fill="x")
        
        # --- Rejilla de productos ---
        # Área desplazable que muestra los productos filtrados en tarjetas
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=1, sticky="nsew")
        
        self.products_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.products_container.pack(fill="both", expand=True)
        
        # Carga inicial
        # Renderiza la lista de productos en la vista al crear la página
        self.update_products()

    def update_price_label(self, value):
        self.price_label.configure(text=f"Precio Máximo: ${int(value)}")
        self.update_products()

    def update_products(self, *args):
        # Limpiar elementos existentes
        # Destruye los widgets actuales antes de volver a poblar la lista filtrada
        for widget in self.products_container.winfo_children():
            widget.destroy()
            
        search_term = self.search_var.get().lower()
        max_price = self.price_slider.get()
        
        filtered = [p for p in MOCK_PRODUCTS if search_term in p['name'].lower() and p['price'] <= max_price]
        
        # Lógica de rejilla (ej.: 3 columnas)
        # Calcula la fila y columna en función del índice para ubicar cada tarjeta
        columns = 3
        for i, product in enumerate(filtered):
            row = i // columns
            col = i % columns
            
            card = ProductCard(self.products_container, product)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

class ProductCard(ctk.CTkFrame):
    def __init__(self, master, product):
        super().__init__(master, fg_color="white", border_width=1, border_color="#D1D5DB")
        
        # Marcador de imagen
        # Para mantener la demo ligera no se cargan imágenes reales; se muestra un bloque de color o texto.
        self.image_area = ctk.CTkLabel(self, text="[IMG]", width=150, height=150, fg_color="#D1D5DB", corner_radius=5, text_color="#854D0E")
        self.image_area.pack(pady=10, padx=10)
        
        self.name_label = ctk.CTkLabel(self, text=product['name'], font=ctk.CTkFont(weight="bold"), wraplength=150, text_color="black")
        self.name_label.pack(pady=5, padx=10)
        
        self.price_label = ctk.CTkLabel(self, text=f"${product['price']}", text_color="#D97706", font=ctk.CTkFont(weight="bold", size=16))
        self.price_label.pack(pady=5)
        
        self.btn = ctk.CTkButton(self, text="Añadir", height=30, fg_color="#F97316", hover_color="#D97706")
        self.btn.pack(pady=10, padx=10)
