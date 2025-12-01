import customtkinter as ctk
from PIL import Image
import os 
from frontend.ui.ecommerce.data import MOCK_PRODUCTS


# --- 1. CONFIGURACIÓN DE RUTA ABSOLUTA ---
# Se requieren 4 pasos atrás (..) para llegar a la raíz del proyecto desde 'pages'.
current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(current_dir, "..", "..", "..", "..", "static", "imagenesProductos")
IMAGE_SIZE = (150, 150) # Tamaño estandarizado para las miniaturas


class ProductsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # --- NUEVA LÓGICA DE CACHE DE IMÁGENES (Ejecutado solo una vez) ---
        # Esto precarga todas las imágenes en la memoria y evita la lentitud en los filtros.
        self.image_cache = self._load_all_images()
        # Inicializa una variable para rastrear la tarea de actualización (Debounce)
        self.update_job = None
        # ------------------------------------------------------------------
        
        # Diseño: barra lateral izquierda para filtros y área de contenido a la derecha
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Panel de filtros (barra lateral) ---
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
        self.search_var = ctk.StringVar()
        # Modificado: llama a la función de debounce
        self.search_var.trace("w", self._debounced_update_products)
        self.search_entry = ctk.CTkEntry(self.filters_frame, placeholder_text="Buscar...", textvariable=self.search_var)
        self.search_entry.pack(pady=10, padx=10, fill="x")
        
        # Rango de precio
        self.price_label = ctk.CTkLabel(self.filters_frame, text="Precio Máximo: $1500", text_color="#854D0E")
        self.price_label.pack(pady=(20, 5), padx=10, anchor="w")
        
        # Modificado: El slider ahora llama a la función de debounce
        self.price_slider = ctk.CTkSlider(self.filters_frame, from_=0, to=1500, command=self.update_price_label, button_color="#F97316", progress_color="#F97316")
        self.price_slider.set(1000)
        self.price_slider.pack(pady=5, padx=10, fill="x")
        
        # --- Rejilla de productos ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=1, sticky="nsew")
        
        self.products_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.products_container.pack(fill="both", expand=True)
        
        # Carga inicial (Llama directamente a la función de ejecución)
        self._run_update_products()

    def _load_all_images(self):
        """Carga todas las imágenes de los productos en un diccionario (cache) al inicio."""
        cache = {}
        for product in MOCK_PRODUCTS:
            image_filename = product.get('image_file')
            if not image_filename:
                continue

            full_image_path = os.path.join(IMAGE_PATH, image_filename)
            
            try:
                # 4. Cargar, redimensionar y crear CTkImage solo una vez
                pil_image = Image.open(full_image_path).resize(IMAGE_SIZE)
                
                ctk_img = ctk.CTkImage(
                    light_image=pil_image, 
                    dark_image=pil_image, 
                    size=IMAGE_SIZE
                )
                cache[image_filename] = ctk_img
                
            except Exception as e:
                # Si falla la carga, guarda None en el caché.
                print(f"Error al cargar la imagen {image_filename} para caché: {e}")
                cache[image_filename] = None
                
        return cache

    def update_price_label(self, value):
        """Actualiza la etiqueta de precio y dispara el debounce."""
        self.price_label.configure(text=f"Precio Máximo: ${int(value)}")
        self._debounced_update_products() # Llama a la función de debounce

    def _debounced_update_products(self, *args):
        """Cancela cualquier actualización pendiente y programa una nueva con retraso (300ms)."""
        if self.update_job is not None:
            # Cancela el trabajo programado anteriormente
            self.after_cancel(self.update_job)
        
        # Programa la ejecución real de la actualización después de 300ms
        self.update_job = self.after(300, self._run_update_products)

    def _run_update_products(self):
        """Limpia la rejilla y la rellena con productos filtrados (el trabajo pesado),
           minimizando el parpadeo (flickering)."""
        
        # 1. Ocultar el contenedor para evitar el parpadeo mientras se destruyen/crean widgets.
        self.products_container.pack_forget()
        
        # 2. Limpiar elementos existentes (Destrucción)
        for widget in self.products_container.winfo_children():
            widget.destroy()
            
        search_term = self.search_var.get().lower()
        max_price = self.price_slider.get()
        
        # Filtrado de datos
        filtered = [p for p in MOCK_PRODUCTS if search_term in p['name'].lower() and p['price'] <= max_price]
        
        # Lógica de rejilla (ej.: 3 columnas)
        columns = 3
        for i, product in enumerate(filtered):
            row = i // columns
            col = i % columns
            
            # OBTENER IMAGEN DEL CACHÉ
            image_filename = product.get('image_file')
            ctk_img = self.image_cache.get(image_filename)
            
            # 2. PASAR LA IMAGEN YA CARGADA AL ProductCard
            card = ProductCard(
                self.products_container, 
                product, 
                ctk_image=ctk_img, 
                image_filename=image_filename
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # 3. Forzar el procesamiento de las tareas de dibujo pendientes.
        # Esto asegura que todos los nuevos widgets se procesen antes de mostrar el contenedor.
        self.products_container.update_idletasks()
        
        # 4. Mostrar el contenedor de productos de nuevo.
        self.products_container.pack(fill="both", expand=True)

class ProductCard(ctk.CTkFrame):
    # 3. ProductCard ahora recibe el objeto CTkImage ya cargado
    def __init__(self, master, product, ctk_image, image_filename):
        super().__init__(master, fg_color="white", border_width=1, border_color="#D1D5DB", width=200, height=350)
        
        self.product = product
        # Almacenar la referencia de la imagen para evitar que Tkinter la elimine
        self.product_ctk_image = ctk_image 
        
        # --- Lógica de Mostrar Imagen ---
        if ctk_image:
            # Mostrar la imagen real (ya cargada)
            self.image_area = ctk.CTkLabel(
                self, 
                text="", 
                image=ctk_image, 
                width=IMAGE_SIZE[0], 
                height=IMAGE_SIZE[1], 
                corner_radius=5
            )
        else:
            # Si la imagen no pudo ser cargada (Error en _load_all_images)
            self.image_area = ctk.CTkLabel(
                self, 
                text=f"[IMG ERROR: {image_filename or 'N/A'}]", 
                width=IMAGE_SIZE[0], height=IMAGE_SIZE[1], 
                fg_color="#FCA5A5", # Fondo rojo claro
                corner_radius=5, 
                text_color="#7F1D1D" # Texto rojo oscuro
            )

        # Empaquetar el área de imagen (sea real o placeholder/error)
        self.image_area.pack(pady=(10, 5), padx=10)
        
        # Nombre del producto
        self.name_label = ctk.CTkLabel(self, text=product['name'], font=ctk.CTkFont(weight="bold"), wraplength=150, text_color="black")
        self.name_label.pack(pady=(5, 0), padx=10)
        
        # Precio
        self.price_label = ctk.CTkLabel(self, text=f"${product['price']}", text_color="#D97706", font=ctk.CTkFont(weight="bold", size=16))
        self.price_label.pack(pady=(5, 10))
        
        # Botón
        self.btn = ctk.CTkButton(self, text="Añadir", height=30, fg_color="#F97316", hover_color="#D97706")
        self.btn.pack(pady=(0, 10), padx=10)