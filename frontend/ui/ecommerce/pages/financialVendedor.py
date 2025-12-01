import customtkinter as ctk
from ..theme_manager import get_color
from backend.DAOs.CuentasDAO import CuentaDAO
from backend.DAOs.VendedoresDAO import VendedorDAO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class FinancialVendedorPage(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="transparent")
        self.usuario = usuario
        self.id_vendedor = None
        
        # Obtener el ID del vendedor desde el usuario
        if self.usuario:
            vendedor = VendedorDAO.obtener_por_id_usuario(self.usuario.id)
            if vendedor:
                self.id_vendedor = vendedor.id
        
        # Verificar si el vendedor tiene cuentas
        if self.id_vendedor and CuentaDAO.vendedor_tiene_cuentas(self.id_vendedor):
            self.render_financial_interface()
        else:
            self.render_setup_screen()
    
    def render_setup_screen(self):
        """Muestra la pantalla de configuración inicial para crear cuentas"""
        # Limpiar el frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Contenedor centrado
        setup_container = ctk.CTkFrame(self, fg_color="transparent")
        setup_container.pack(expand=True)
        
        # Icono o título
        title = ctk.CTkLabel(
            setup_container, 
            text="🏦 Configuración Inicial", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#111827"
        )
        title.pack(pady=(0, 20))
        
        # Mensaje informativo
        message = ctk.CTkLabel(
            setup_container,
            text="Necesitas crear las cuentas esenciales para tu negocio\nantes de poder ver tus finanzas.",
            font=ctk.CTkFont(size=16),
            text_color="#6B7280",
            justify="center"
        )
        message.pack(pady=(0, 40))
        
        # Botón grande para crear cuentas
        create_btn = ctk.CTkButton(
            setup_container,
            text="Crear Cuentas Esenciales",
            command=self.crear_cuentas_iniciales,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=get_color('success'),
            hover_color="#059669",
            height=60,
            width=300
        )
        create_btn.pack()
        
        # Información adicional
        info = ctk.CTkLabel(
            setup_container,
            text="Se crearán las siguientes cuentas:\n• Ingresos\n• Efectivo\n• Capital Social\n• Utilidades Retenidas\n• Gastos de Ventas",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF",
            justify="center"
        )
        info.pack(pady=(30, 0))
    
    def crear_cuentas_iniciales(self):
        """Crea las cuentas esenciales del vendedor"""
        if not self.id_vendedor:
            print("Error: No se pudo obtener el ID del vendedor")
            return
        
        # Crear las cuentas
        exito = CuentaDAO.crear_cuentas_esenciales_vendedor(self.id_vendedor)
        
        if exito:
            # Mostrar mensaje de éxito y recargar la interfaz
            self.mostrar_mensaje_exito()
        else:
            # Mostrar mensaje de error
            self.mostrar_mensaje_error()
    
    def mostrar_mensaje_exito(self):
        """Muestra un mensaje de éxito y recarga la interfaz"""
        # Popup de éxito
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x200")
        popup.title("¡Éxito!")
        
        ctk.CTkLabel(
            popup, 
            text="✅ Cuentas creadas exitosamente", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=get_color('success')
        ).pack(pady=30)
        
        ctk.CTkLabel(
            popup,
            text="Ahora puedes comenzar a gestionar\ntus finanzas.",
            font=ctk.CTkFont(size=14),
            text_color="#6B7280"
        ).pack(pady=10)
        
        ctk.CTkButton(
            popup,
            text="Continuar",
            command=lambda: [popup.destroy(), self.render_financial_interface()],
            fg_color=get_color('accent')
        ).pack(pady=20)
    
    def mostrar_mensaje_error(self):
        """Muestra un mensaje de error"""
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x150")
        popup.title("Error")
        
        ctk.CTkLabel(
            popup, 
            text="❌ Error al crear las cuentas", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#EF4444"
        ).pack(pady=30)
        
        ctk.CTkButton(
            popup,
            text="Cerrar",
            command=popup.destroy,
            fg_color="#6B7280"
        ).pack(pady=10)
    
    def render_financial_interface(self):
        """Renderiza la interfaz financiera completa"""
        # Limpiar el frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(self.header_frame, text="Análisis Financiero - Vendedor", font=ctk.CTkFont(size=22, weight="bold"), text_color="#111827")
        title.pack(side="left")
        
        # Header Buttons
        btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Exportar Reporte", command=self.export_report, fg_color=get_color('success')).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Interpretar", command=self.show_interpretations, fg_color=get_color('accent')).pack(side="left", padx=6)
        
        # --- Pestañas ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#F97316", segmented_button_selected_hover_color="#D97706")
        self.tabview.pack(fill="both", expand=True)
        
        self.tabs = {
            "Cuentas": self.tabview.add("Cuentas"),
            "Gestionar": self.tabview.add("Agregar/Modificar Cuentas"),
            "Balance": self.tabview.add("Balance General"),
            "Resultados": self.tabview.add("Estado de Resultados"),
            "Origen": self.tabview.add("Origen y Aplicación"),
            "Razones": self.tabview.add("Razones Financieras"),
            "Flujos": self.tabview.add("Flujos de Efectivo"),
            "Graficos": self.tabview.add("Gráficos"),
            "Proforma": self.tabview.add("Proforma")
        }
        
        # Cargar la pestaña de Cuentas con las cuentas del vendedor
        self.load_cuentas_tab()
        
        # Cargar la pestaña de Gestionar Cuentas
        self.load_gestionar_tab()
        
        # Cargar la pestaña de Balance General
        self.load_balance_tab()
        
        # Cargar la pestaña de Estado de Resultados
        self.load_resultados_tab()
        
        # Cargar la pestaña de Origen y Aplicación
        self.load_origen_aplicacion_tab()
        
        # Cargar la pestaña de Razones Financieras
        self.load_razones_tab()
        
        # Cargar la pestaña de Flujos de Efectivo
        self.load_flujos_tab()
        
        # Cargar la pestaña de Gráficos
        self.load_graficos_tab()
        
        # Cargar la pestaña de Proforma
        self.load_proforma_tab()
        
        # Contenido placeholder para las demás pestañas
        for tab_name, tab in self.tabs.items():
            if tab_name in ["Cuentas", "Gestionar", "Balance", "Resultados", "Origen", "Razones", "Flujos", "Graficos", "Proforma"]:
                continue
                
            placeholder = ctk.CTkFrame(tab, fg_color="transparent")
            placeholder.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                placeholder, 
                text=f"📊 {tab_name}", 
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#374151"
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                placeholder, 
                text="Esta sección mostrará la información financiera de tu negocio.\nPróximamente disponible.", 
                font=ctk.CTkFont(size=14),
                text_color="#6B7280"
            ).pack()

    def load_flujos_tab(self):
        """Carga la pestaña de Flujos de Efectivo (Directo e Indirecto)"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Flujos"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        # Contenedor principal
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Estado de Flujos de Efectivo",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            main_frame,
            text="Comparativo: Método Directo vs Método Indirecto",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(pady=(0, 20))
        
        # --- OBTENCIÓN DE DATOS ---
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        def get_val(nombre_parcial, tipo_id=None):
            total = 0.0
            for c in cuentas:
                if tipo_id and c.id_tipo_cuenta != tipo_id:
                    continue
                if nombre_parcial.lower() in c.nombre_cuenta.lower():
                    total += float(c.saldo_actual)
            return total
            
        def get_total_tipo(tipo_id):
            return sum(float(c.saldo_actual) for c in cuentas if c.id_tipo_cuenta == tipo_id)

        # Datos Operativos
        ingresos = get_total_tipo(6)
        gastos_op = get_total_tipo(7)
        intereses = get_total_tipo(8)
        
        # Utilidad Neta (Simplificada sin IR para este ejemplo, o calculada igual que en Resultados)
        utilidad_antes_ir = ingresos - gastos_op - intereses
        vendedor = VendedorDAO.obtener_por_id_usuario(self.usuario.id)
        ir = 0
        if vendedor and vendedor.es_contribuyente and utilidad_antes_ir > 0:
            ir = utilidad_antes_ir * 0.30
        utilidad_neta = utilidad_antes_ir - ir
        
        # Datos de Balance (Variaciones asumiendo anterior = 0)
        # Activos
        depreciacion = get_val("depreciacion") # Gasto virtual
        aumento_cxc = get_val("clientes", 1) + get_val("cuentas por cobrar", 1)
        aumento_inventario = get_val("inventario", 1)
        
        # Pasivos
        aumento_cxp = get_val("proveedores", 3) + get_val("cuentas por pagar", 3)
        
        # Inversión (Activos No Corrientes brutos aprox)
        # Asumimos que todo el activo no corriente actual fue comprado este año (anterior=0)
        # Excluyendo depreciación acumulada si estuviera en el activo (normalmente es negativa o cuenta aparte)
        # Aquí simplificamos: Variación Activo No Corriente Neto + Depreciación del periodo = Inversión Bruta
        activos_no_corr_neto = get_total_tipo(2)
        inversion_activos = activos_no_corr_neto # Si asumimos anterior 0
        
        # Financiamiento
        aumento_capital = get_total_tipo(5) - get_val("utilidades retenidas", 5) - get_val("resultado", 5) # Capital social aportado
        aumento_deuda_lp = get_total_tipo(4)
        
        # --- CÁLCULOS ---
        
        # MÉTODO DIRECTO
        # Operación: Cobros - Pagos
        # Cobros = Ventas - Aumento CxC
        cobros_clientes = ingresos - aumento_cxc
        
        # Pagos Proveedores = Costo Ventas + Aumento Inv - Aumento CxP
        # Como no tenemos Costo Ventas separado explícitamente siempre, usamos Gastos Op como proxy de salidas de efectivo
        # Ajuste: Gastos - Depreciación (no efectivo) - Aumento CxP + Aumento Inv (si es costo)
        # Simplificación para el ejercicio: Pagos = Gastos (sin dep) + Aumento Inv - Aumento CxP
        pagos_operativos = (gastos_op - depreciacion) + aumento_inventario - aumento_cxp
        pago_intereses = intereses
        pago_impuestos = ir
        
        flujo_op_directo = cobros_clientes - pagos_operativos - pago_intereses - pago_impuestos
        
        # Inversión
        flujo_inv = -inversion_activos
        
        # Financiamiento
        flujo_fin = aumento_capital + aumento_deuda_lp
        
        flujo_neto_directo = flujo_op_directo + flujo_inv + flujo_fin
        
        # MÉTODO INDIRECTO
        # Utilidad Neta + Partidas Virtuales + Variaciones Capital Trabajo
        partidas_virtuales = depreciacion
        
        # Variaciones (Signos: Aumento Activo (-), Aumento Pasivo (+))
        var_cxc = -aumento_cxc
        var_inv = -aumento_inventario
        var_cxp = aumento_cxp
        
        flujo_op_indirecto = utilidad_neta + partidas_virtuales + var_cxc + var_inv + var_cxp
        
        # Inversión y Financiamiento (Iguales)
        flujo_neto_indirecto = flujo_op_indirecto + flujo_inv + flujo_fin
        
        # --- RENDERIZADO ---
        
        split_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        split_frame.pack(fill="both", expand=True)
        
        # Helper para filas
        def add_row(parent, text, amount, is_bold=False, is_total=False):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(fill="x", pady=2)
            font = ctk.CTkFont(weight="bold" if (is_bold or is_total) else "normal", size=13 if is_total else 12)
            color = "#111827" if (is_bold or is_total) else "#374151"
            ctk.CTkLabel(f, text=text, font=font, text_color=color, anchor="w").pack(side="left")
            if amount is not None:
                ctk.CTkLabel(f, text=f"${amount:,.2f}", font=font, text_color=color, anchor="e").pack(side="right")

        # IZQUIERDA: MÉTODO DIRECTO
        left = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", corner_radius=8)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left, text="MÉTODO DIRECTO", font=ctk.CTkFont(weight="bold", size=14), text_color="#059669").pack(pady=10)
        
        add_row(left, "ACTIVIDADES DE OPERACIÓN", None, is_bold=True)
        add_row(left, "+ Cobros a Clientes", cobros_clientes)
        add_row(left, "- Pagos Operativos", pagos_operativos)
        add_row(left, "- Pago de Intereses", pago_intereses)
        add_row(left, "- Pago de Impuestos", pago_impuestos)
        ctk.CTkFrame(left, height=1, fg_color="#E5E7EB").pack(fill="x", pady=5)
        add_row(left, "Flujo Neto de Operación", flujo_op_directo, is_total=True)
        
        ctk.CTkLabel(left, text="", height=10).pack()
        
        add_row(left, "ACTIVIDADES DE INVERSIÓN", None, is_bold=True)
        add_row(left, "- Compra de Activos No Corr.", inversion_activos)
        ctk.CTkFrame(left, height=1, fg_color="#E5E7EB").pack(fill="x", pady=5)
        add_row(left, "Flujo Neto de Inversión", flujo_inv, is_total=True)
        
        ctk.CTkLabel(left, text="", height=10).pack()
        
        add_row(left, "ACTIVIDADES DE FINANCIAMIENTO", None, is_bold=True)
        add_row(left, "+ Aumento de Capital", aumento_capital)
        add_row(left, "+ Préstamos Largo Plazo", aumento_deuda_lp)
        ctk.CTkFrame(left, height=1, fg_color="#E5E7EB").pack(fill="x", pady=5)
        add_row(left, "Flujo Neto de Financiamiento", flujo_fin, is_total=True)
        
        ctk.CTkFrame(left, height=2, fg_color="#059669").pack(fill="x", pady=15)
        add_row(left, "VARIACIÓN NETA DE EFECTIVO", flujo_neto_directo, is_total=True)

        # DERECHA: MÉTODO INDIRECTO
        right = ctk.CTkFrame(split_frame, fg_color="#FFFFFF", corner_radius=8)
        right.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(right, text="MÉTODO INDIRECTO", font=ctk.CTkFont(weight="bold", size=14), text_color="#2563EB").pack(pady=10)
        
        add_row(right, "ACTIVIDADES DE OPERACIÓN", None, is_bold=True)
        add_row(right, "Utilidad Neta", utilidad_neta)
        add_row(right, "+ Depreciaciones y Amort.", partidas_virtuales)
        add_row(right, "(- Aumento / + Dism.) CxC", var_cxc)
        add_row(right, "(- Aumento / + Dism.) Inventario", var_inv)
        add_row(right, "(+ Aumento / - Dism.) CxP", var_cxp)
        ctk.CTkFrame(right, height=1, fg_color="#E5E7EB").pack(fill="x", pady=5)
        add_row(right, "Flujo Neto de Operación", flujo_op_indirecto, is_total=True)
        
        ctk.CTkLabel(right, text="", height=10).pack()
        
        add_row(right, "ACTIVIDADES DE INVERSIÓN", None, is_bold=True)
        add_row(right, "Flujo Neto de Inversión", flujo_inv) # Resumido
        
        ctk.CTkLabel(right, text="", height=10).pack()
        
        add_row(right, "ACTIVIDADES DE FINANCIAMIENTO", None, is_bold=True)
        add_row(right, "Flujo Neto de Financiamiento", flujo_fin) # Resumido
        
        ctk.CTkFrame(right, height=2, fg_color="#2563EB").pack(fill="x", pady=15)
        add_row(right, "VARIACIÓN NETA DE EFECTIVO", flujo_neto_indirecto, is_total=True)

    def load_origen_aplicacion_tab(self):
        """Carga la pestaña de Estado de Origen y Aplicación de Fondos"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Origen"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Estado de Origen y Aplicación de Fondos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame,
            text="Comparativo: Período Anterior (Asumido 0) vs Período Actual",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(pady=(0, 10))
        
        # Obtener cuentas
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        origenes = []
        aplicaciones = []
        total_origen = 0
        total_aplicacion = 0
        
        for cuenta in cuentas:
            # Asumimos saldo anterior = 0
            saldo_anterior = 0
            saldo_actual = cuenta.saldo_actual
            variacion = saldo_actual - saldo_anterior
            
            if variacion == 0:
                continue
                
            tipo = cuenta.id_tipo_cuenta
            
            # Clasificación
            # Activos (1, 2): Aumento -> Aplicación, Disminución -> Origen
            # Pasivos (3, 4) y Capital (5): Aumento -> Origen, Disminución -> Aplicación
            
            es_origen = False
            
            if tipo in [1, 2]: # Activos
                if variacion < 0: es_origen = True # Disminución de activo
            elif tipo in [3, 4, 5]: # Pasivos y Capital
                if variacion > 0: es_origen = True # Aumento de pasivo/capital
                
            monto = abs(variacion)
            
            item = {"cuenta": cuenta.nombre_cuenta, "monto": monto}
            
            if es_origen:
                origenes.append(item)
                total_origen += monto
            else:
                aplicaciones.append(item)
                total_aplicacion += monto
                
        # Renderizar Tablas lado a lado
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Tabla Orígenes
        left_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=8)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="ORÍGENES (Fuentes)", font=ctk.CTkFont(weight="bold"), text_color="#059669").pack(pady=10)
        
        for item in origenes:
            row = ctk.CTkFrame(left_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=item["cuenta"], anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"${item['monto']:,.2f}", anchor="e").pack(side="right")
            
        ctk.CTkFrame(left_frame, height=2, fg_color="#E5E7EB").pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(left_frame, text=f"TOTAL ORÍGENES: ${total_origen:,.2f}", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 10))

        # Tabla Aplicaciones
        right_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=8)
        right_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(right_frame, text="APLICACIONES (Usos)", font=ctk.CTkFont(weight="bold"), text_color="#DC2626").pack(pady=10)
        
        for item in aplicaciones:
            row = ctk.CTkFrame(right_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=item["cuenta"], anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"${item['monto']:,.2f}", anchor="e").pack(side="right")
            
        ctk.CTkFrame(right_frame, height=2, fg_color="#E5E7EB").pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(right_frame, text=f"TOTAL APLICACIONES: ${total_aplicacion:,.2f}", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 10))

    def load_razones_tab(self):
        """Carga la pestaña de Razones Financieras"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Razones"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Razones Financieras y Análisis Dupont",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        # --- OBTENCIÓN DE DATOS ---
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        # Helper para sumar por tipo y/o nombre
        def sum_cuentas(tipos, nombre_contiene=None, nombre_excluye=None):
            total = 0.0
            for c in cuentas:
                if c.id_tipo_cuenta in tipos:
                    if nombre_contiene and nombre_contiene.lower() not in c.nombre_cuenta.lower():
                        continue
                    if nombre_excluye and nombre_excluye.lower() in c.nombre_cuenta.lower():
                        continue
                    total += float(c.saldo_actual)
            return total

        # Variables Base
        activos_corrientes = sum_cuentas([1])
        activos_totales = sum_cuentas([1, 2])
        pasivos_corrientes = sum_cuentas([3])
        pasivos_totales = sum_cuentas([3, 4])
        capital_total = sum_cuentas([5])
        
        ventas = sum_cuentas([6]) # Ingresos
        costo_ventas = sum_cuentas([7], "costo") # Asumiendo que "Costo" está en el nombre
        gastos_operativos = sum_cuentas([7], nombre_excluye="costo") # Gastos op excluyendo costo
        intereses = sum_cuentas([8]) # Gastos Financieros
        
        inventario = sum_cuentas([1], "inventario")
        cxc = sum_cuentas([1], "clientes") + sum_cuentas([1], "cuentas por cobrar")
        cxp = sum_cuentas([3], "proveedores") + sum_cuentas([3], "cuentas por pagar")
        
        # Cálculos de Resultados
        utilidad_bruta = ventas - costo_ventas
        ebit = utilidad_bruta - gastos_operativos # Earnings Before Interest and Taxes
        ebt = ebit - intereses # Earnings Before Taxes
        
        # Impuestos (Simulado 30% si es contribuyente, o 0)
        vendedor = VendedorDAO.obtener_por_id_usuario(self.usuario.id)
        impuestos = 0
        if vendedor and vendedor.es_contribuyente and ebt > 0:
            impuestos = ebt * 0.30
            
        utilidad_neta = ebt - impuestos
        
        # --- RENDERIZADO ---
        
        def add_section_title(text):
            ctk.CTkLabel(main_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"), anchor="w", text_color="#1F2937").pack(fill="x", pady=(20, 5))

        def add_ratio_card(parent, title, value, formula, interpretation, color="#2563EB"):
            card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8)
            card.pack(fill="x", pady=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=(10, 5))
            
            ctk.CTkLabel(header, text=title, font=ctk.CTkFont(weight="bold", size=14)).pack(side="left")
            ctk.CTkLabel(header, text=f"{value}", font=ctk.CTkFont(weight="bold", size=14), text_color=color).pack(side="right")
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=(0, 10))
            
            ctk.CTkLabel(content, text=f"Fórmula: {formula}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(anchor="w")
            ctk.CTkLabel(content, text=f"{interpretation}", font=ctk.CTkFont(size=12), text_color="#374151", wraplength=600, justify="left").pack(anchor="w", pady=(5, 0))

        # 1. LIQUIDEZ
        add_section_title("1. Razones de Liquidez")
        
        # Liquidez Corriente
        liq_corr = activos_corrientes / pasivos_corrientes if pasivos_corrientes else 0
        add_ratio_card(main_frame, "Liquidez Corriente", f"{liq_corr:.2f}", "AC / PC", 
                      "Capacidad de cubrir deudas a corto plazo." + (" Óptimo." if liq_corr >= 1 else " Riesgo de iliquidez."))
        
        # Prueba Ácida
        prueba_acida = (activos_corrientes - inventario) / pasivos_corrientes if pasivos_corrientes else 0
        add_ratio_card(main_frame, "Prueba Ácida", f"{prueba_acida:.2f}", "(AC - Inventario) / PC", 
                      "Capacidad de pago inmediata sin depender de la venta de inventarios.")
        
        # Capital de Trabajo Neto (CNT)
        cnt = activos_corrientes - pasivos_corrientes
        add_ratio_card(main_frame, "Capital de Trabajo Neto (CNT)", f"${cnt:,.2f}", "AC - PC", 
                      "Dinero disponible para operar tras pagar deudas a corto plazo.")
        
        # Capital de Trabajo Neto Operativo (CNO)
        cno = (cxc + inventario) - cxp
        add_ratio_card(main_frame, "Capital de Trabajo Neto Operativo (CNO)", f"${cno:,.2f}", "(CxC + Inv) - CxP Operativa", 
                      "Dinero necesario para sostener la operación diaria del negocio.")

        # 2. ACTIVIDAD (EFICIENCIA)
        add_section_title("2. Razones de Actividad")
        
        # Rotación de Inventario
        rot_inv = costo_ventas / inventario if inventario else 0
        add_ratio_card(main_frame, "Rotación de Inventario", f"{rot_inv:.2f} veces", "Costo Ventas / Inventario", 
                      "Veces que se renueva el inventario en el período.")
        
        # Período Promedio de Cobro
        ppc = (cxc / ventas * 360) if ventas else 0
        add_ratio_card(main_frame, "Período Promedio de Cobro", f"{ppc:.0f} días", "(CxC / Ventas) * 360", 
                      "Días promedio que se tarda en cobrar a los clientes.")
        
        # Rotación de Activos Totales
        rot_activos = ventas / activos_totales if activos_totales else 0
        add_ratio_card(main_frame, "Rotación de Activos Totales", f"{rot_activos:.2f}", "Ventas / Activos Totales", 
                      "Eficiencia de los activos para generar ventas.")

        # 3. ENDEUDAMIENTO
        add_section_title("3. Razones de Endeudamiento")
        
        # Índice de Endeudamiento (Pasivo/Activo)
        end_total = (pasivos_totales / activos_totales * 100) if activos_totales else 0
        add_ratio_card(main_frame, "Índice de Endeudamiento", f"{end_total:.2f}%", "Pasivo Total / Activo Total", 
                      f"Porcentaje de activos financiados por terceros.")
        
        # Cobertura de Intereses
        cob_int = ebit / intereses if intereses else 0
        cob_int_str = f"{cob_int:.2f}" if intereses else "N/A (Sin intereses)"
        add_ratio_card(main_frame, "Cobertura de Intereses", cob_int_str, "EBIT / Intereses", 
                      "Capacidad para pagar los intereses con la utilidad operativa.")

        # 4. RENTABILIDAD
        add_section_title("4. Razones de Rentabilidad")
        
        # Margen Bruto
        margen_bruto = (utilidad_bruta / ventas * 100) if ventas else 0
        add_ratio_card(main_frame, "Margen de Utilidad Bruta", f"{margen_bruto:.2f}%", "Utilidad Bruta / Ventas", 
                      "Ganancia directa por venta antes de gastos operativos.")
        
        # Margen Neto
        margen_neto = (utilidad_neta / ventas * 100) if ventas else 0
        add_ratio_card(main_frame, "Margen de Utilidad Neta", f"{margen_neto:.2f}%", "Utilidad Neta / Ventas", 
                      "Ganancia final por cada dólar vendido.")
        
        # ROA
        roa = (utilidad_neta / activos_totales * 100) if activos_totales else 0
        add_ratio_card(main_frame, "ROA (Rentabilidad sobre Activos)", f"{roa:.2f}%", "Utilidad Neta / Activos", 
                      "Rendimiento generado por cada dólar invertido en activos.")
        
        # ROE
        roe = (utilidad_neta / capital_total * 100) if capital_total else 0
        add_ratio_card(main_frame, "ROE (Rentabilidad sobre Capital)", f"{roe:.2f}%", "Utilidad Neta / Capital", 
                      "Rendimiento para los accionistas.")

        # 5. ANÁLISIS DUPONT
        add_section_title("5. Análisis Dupont")
        
        dupont_frame = ctk.CTkFrame(main_frame, fg_color="#F0F9FF", corner_radius=8, border_width=1, border_color="#BAE6FD")
        dupont_frame.pack(fill="x", pady=5)
        
        # Dupont 3 Pasos
        # ROE = Margen Neto x Rotación Activos x Multiplicador Capital
        mult_capital = activos_totales / capital_total if capital_total else 0
        
        ctk.CTkLabel(dupont_frame, text="Dupont (3 Pasos)", font=ctk.CTkFont(weight="bold", size=14), text_color="#0369A1").pack(anchor="w", padx=15, pady=(15, 5))
        
        d3_text = f"ROE ({roe:.2f}%) = Margen Neto ({margen_neto:.2f}%) × Rotación Activos ({rot_activos:.2f}) × Mult. Capital ({mult_capital:.2f})"
        ctk.CTkLabel(dupont_frame, text=d3_text, font=ctk.CTkFont(size=12), padx=15).pack(anchor="w", pady=(0, 10))
        
        # Dupont 5 Pasos
        # ROE = (Utilidad Neta / EBT) x (EBT / EBIT) x (EBIT / Ventas) x (Ventas / Activos) x (Activos / Capital)
        #       Tax Burden            Interest Burden  Op. Margin       Asset Turnover      Fin. Leverage
        
        tax_burden = utilidad_neta / ebt if ebt else 1
        interest_burden = ebt / ebit if ebit else 1
        op_margin = ebit / ventas if ventas else 0
        
        ctk.CTkLabel(dupont_frame, text="Dupont (5 Pasos - Extendido)", font=ctk.CTkFont(weight="bold", size=14), text_color="#0369A1").pack(anchor="w", padx=15, pady=(10, 5))
        
        d5_text = (f"ROE = Carga Fiscal ({tax_burden:.2f}) × Carga Intereses ({interest_burden:.2f}) × "
                   f"Margen Op. ({op_margin:.2f}) × Rot. Activos ({rot_activos:.2f}) × Apalancamiento ({mult_capital:.2f})")
        ctk.CTkLabel(dupont_frame, text=d5_text, font=ctk.CTkFont(size=12), padx=15).pack(anchor="w", pady=(0, 15))
            
    def load_balance_tab(self):
        """Carga la pestaña de Balance General"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Balance"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        # Contenedor principal
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Balance General",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        # Obtener cuentas
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        # Clasificar cuentas
        activos_corrientes = [c for c in cuentas if c.id_tipo_cuenta == 1]
        activos_no_corrientes = [c for c in cuentas if c.id_tipo_cuenta == 2]
        pasivos_corrientes = [c for c in cuentas if c.id_tipo_cuenta == 3]
        pasivos_no_corrientes = [c for c in cuentas if c.id_tipo_cuenta == 4]
        capital = [c for c in cuentas if c.id_tipo_cuenta == 5]
        
        # Calcular totales
        total_activos_corr = sum(c.saldo_actual for c in activos_corrientes)
        total_activos_no_corr = sum(c.saldo_actual for c in activos_no_corrientes)
        total_activos = total_activos_corr + total_activos_no_corr
        
        total_pasivos_corr = sum(c.saldo_actual for c in pasivos_corrientes)
        total_pasivos_no_corr = sum(c.saldo_actual for c in pasivos_no_corrientes)
        total_pasivos = total_pasivos_corr + total_pasivos_no_corr
        
        total_capital = sum(c.saldo_actual for c in capital)
        
        total_pasivo_capital = total_pasivos + total_capital
        
        # Alerta de desbalance
        if abs(total_activos - total_pasivo_capital) > 0.01:
            alert_frame = ctk.CTkFrame(main_frame, fg_color="#FEE2E2", corner_radius=8, border_width=1, border_color="#EF4444")
            alert_frame.pack(fill="x", pady=(0, 20))
            
            mayor = "ACTIVOS" if total_activos > total_pasivo_capital else "PASIVO + CAPITAL"
            diferencia = abs(total_activos - total_pasivo_capital)
            
            ctk.CTkLabel(
                alert_frame,
                text=f"⚠️ ERROR FATAL: CUENTAS DESBALANCEADAS",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#B91C1C"
            ).pack(pady=(10, 5))
            
            ctk.CTkLabel(
                alert_frame,
                text=f"Mayor: {mayor} (Diferencia: ${diferencia:,.2f})\nAjuste las cuentas consultando a soporte técnico",
                text_color="#B91C1C"
            ).pack(pady=(0, 10))

        # Tabla de Balance
        # Headers
        headers_frame = ctk.CTkFrame(main_frame, fg_color="#F3F4F6")
        headers_frame.pack(fill="x", pady=5)
        
        cols = ["Cuenta", "Monto Ant ($0)", "Vert Ant %", "Monto Act", "Vert Act %", "Var $", "Var %"]
        widths = [200, 100, 80, 100, 80, 100, 80]
        
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                headers_frame,
                text=col,
                font=ctk.CTkFont(weight="bold", size=11),
                width=widths[i],
                anchor="w" if i == 0 else "e"
            ).grid(row=0, column=i, padx=5, pady=5)
            
        def add_section(title, accounts, total_base_act, total_base_ant=0, is_total=False):
            # Título de sección
            ctk.CTkLabel(
                main_frame,
                text=title,
                font=ctk.CTkFont(weight="bold", size=14 if is_total else 12),
                text_color="#111827" if is_total else "#4B5563",
                anchor="w"
            ).pack(fill="x", pady=(10 if is_total else 5, 2))
            
            # Cuentas
            for cuenta in accounts:
                row = ctk.CTkFrame(main_frame, fg_color="transparent")
                row.pack(fill="x")
                
                # Datos Actuales
                monto_act = float(cuenta.saldo_actual)
                vert_act = (monto_act / float(total_base_act) * 100) if total_base_act else 0
                
                # Datos Anteriores (Simulados en 0)
                monto_ant = 0.0
                vert_ant = 0.0 # (0 / 0 * 100)
                
                # Variaciones
                var_abs = monto_act - monto_ant
                # Var %: Si anterior es 0 y actual > 0, es 100% (o infinito, mostramos 100% para indicar nuevo)
                if monto_ant == 0:
                    var_pct = 100.0 if monto_act != 0 else 0.0
                else:
                    var_pct = (var_abs / monto_ant) * 100
                
                values = [
                    (cuenta.nombre_cuenta, "w"),
                    (f"${monto_ant:,.2f}", "e"),
                    (f"{vert_ant:.1f}%", "e"),
                    (f"${monto_act:,.2f}", "e"),
                    (f"{vert_act:.1f}%", "e"),
                    (f"${var_abs:,.2f}", "e"),
                    (f"{var_pct:.1f}%", "e")
                ]
                
                for i, (val, anchor) in enumerate(values):
                    ctk.CTkLabel(
                        row,
                        text=val,
                        width=widths[i],
                        anchor=anchor,
                        font=ctk.CTkFont(size=12)
                    ).grid(row=0, column=i, padx=5, pady=2)
        
        def add_total_row(label, amount_act, amount_ant=0):
            row = ctk.CTkFrame(main_frame, fg_color="#F9FAFB")
            row.pack(fill="x", pady=5)
            
            # Calcular variaciones totales
            var_abs = amount_act - amount_ant
            var_pct = 100.0 if amount_ant == 0 and amount_act != 0 else 0.0
            
            values = [
                (label, "w"),
                (f"${amount_ant:,.2f}", "e"),
                ("-", "e"), # Vert Ant no aplica a totales o es 100%
                (f"${amount_act:,.2f}", "e"),
                ("-", "e"), # Vert Act no aplica a totales o es 100%
                (f"${var_abs:,.2f}", "e"),
                (f"{var_pct:.1f}%", "e")
            ]
            
            for i, (val, anchor) in enumerate(values):
                font_weight = "bold"
                ctk.CTkLabel(row, text=val, font=ctk.CTkFont(weight=font_weight, size=11), width=widths[i], anchor=anchor).grid(row=0, column=i, padx=5, pady=5)
            
        # ACTIVOS
        ctk.CTkLabel(main_frame, text="ACTIVOS", font=ctk.CTkFont(size=16, weight="bold"), text_color="#059669", anchor="w").pack(fill="x", pady=(10, 5))
        
        add_section("Activos Corrientes", activos_corrientes, total_activos)
        add_section("Activos No Corrientes", activos_no_corrientes, total_activos)
        add_total_row("TOTAL ACTIVOS", total_activos)
        
        # PASIVOS
        ctk.CTkLabel(main_frame, text="PASIVOS", font=ctk.CTkFont(size=16, weight="bold"), text_color="#DC2626", anchor="w").pack(fill="x", pady=(20, 5))
        
        add_section("Pasivos Corrientes", pasivos_corrientes, total_activos) # Base vertical siempre es Activos
        add_section("Pasivos No Corrientes", pasivos_no_corrientes, total_activos)
        add_total_row("TOTAL PASIVOS", total_pasivos)
        
        # CAPITAL
        ctk.CTkLabel(main_frame, text="CAPITAL", font=ctk.CTkFont(size=16, weight="bold"), text_color="#2563EB", anchor="w").pack(fill="x", pady=(20, 5))
        
        add_section("Capital Contable", capital, total_activos)
        add_total_row("TOTAL CAPITAL", total_capital)
        
        # TOTAL PASIVO + CAPITAL
        add_total_row("TOTAL PASIVO + CAPITAL", total_pasivo_capital)
        
    def load_resultados_tab(self):
        """Carga la pestaña de Estado de Resultados"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Resultados"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        main_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Estado de Resultados",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        # Obtener datos
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        ingresos = [c for c in cuentas if c.id_tipo_cuenta == 6]
        gastos = [c for c in cuentas if c.id_tipo_cuenta in [7, 8]]
        
        total_ingresos = sum(c.saldo_actual for c in ingresos)
        total_gastos = sum(c.saldo_actual for c in gastos)
        utilidad_antes_ir = total_ingresos - total_gastos
        
        # Calcular IR
        vendedor = VendedorDAO.obtener_por_id_usuario(self.usuario.id)
        ir = 0
        if vendedor and vendedor.es_contribuyente and utilidad_antes_ir > 0:
            ir = utilidad_antes_ir * 0.30
            
        utilidad_neta = utilidad_antes_ir - ir
        
        # Headers
        headers_frame = ctk.CTkFrame(main_frame, fg_color="#F3F4F6")
        headers_frame.pack(fill="x", pady=5)
        
        cols = ["Cuenta", "Monto Ant ($0)", "Vert Ant %", "Monto Act", "Vert Act %", "Var $", "Var %"]
        widths = [200, 100, 80, 100, 80, 100, 80]
        
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                headers_frame,
                text=col,
                font=ctk.CTkFont(weight="bold", size=11),
                width=widths[i],
                anchor="w" if i == 0 else "e"
            ).grid(row=0, column=i, padx=5, pady=5)

        # Tabla Actual
        def add_row(parent, label, amount_act, total_base_act, amount_ant=0, is_total=False, is_sub=False):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=0, pady=2)
            
            font = ctk.CTkFont(weight="bold" if is_total else "normal", size=12)
            color = "#111827" if is_total else "#374151"
            
            # Cálculos
            amount_act = float(amount_act)
            total_base_act = float(total_base_act)
            
            vert_act = (amount_act / total_base_act * 100) if total_base_act else 0
            vert_ant = 0.0 # Base 0
            
            var_abs = amount_act - amount_ant
            var_pct = 100.0 if amount_ant == 0 and amount_act != 0 else 0.0
            
            values = [
                (label, "w"),
                (f"${amount_ant:,.2f}", "e"),
                (f"{vert_ant:.1f}%", "e"),
                (f"${amount_act:,.2f}", "e"),
                (f"{vert_act:.1f}%", "e"),
                (f"${var_abs:,.2f}", "e"),
                (f"{var_pct:.1f}%", "e")
            ]
            
            for i, (val, anchor) in enumerate(values):
                ctk.CTkLabel(
                    row,
                    text=val,
                    font=font,
                    text_color=color,
                    width=widths[i],
                    anchor=anchor
                ).grid(row=0, column=i, padx=5, pady=2)

        # Ingresos
        ctk.CTkLabel(main_frame, text="INGRESOS", font=ctk.CTkFont(weight="bold"), text_color="#059669", anchor="w").pack(fill="x", padx=10, pady=(10, 5))
        for c in ingresos:
            add_row(main_frame, c.nombre_cuenta, c.saldo_actual, total_ingresos)
        add_row(main_frame, "Total Ingresos", total_ingresos, total_ingresos, is_total=True)
        
        # Gastos
        ctk.CTkLabel(main_frame, text="GASTOS", font=ctk.CTkFont(weight="bold"), text_color="#DC2626", anchor="w").pack(fill="x", padx=10, pady=(15, 5))
        for c in gastos:
            add_row(main_frame, c.nombre_cuenta, c.saldo_actual, total_ingresos) # Base vertical ingresos
        add_row(main_frame, "Total Gastos", total_gastos, total_ingresos, is_total=True)
        
        # Resultados
        ctk.CTkFrame(main_frame, height=2, fg_color="#E5E7EB").pack(fill="x", pady=10, padx=10)
        
        add_row(main_frame, "Utilidad Antes de IR", utilidad_antes_ir, total_ingresos, is_total=True)
        if ir > 0:
            add_row(main_frame, "Impuesto sobre Renta (30%)", ir, total_ingresos)
        
        ctk.CTkLabel(main_frame, text=f"UTILIDAD NETA: ${utilidad_neta:,.2f}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2563EB").pack(pady=15)
        
        # Simulación de cierre (visual)
        sim_frame = ctk.CTkFrame(main_frame, fg_color="#EFF6FF", corner_radius=8)
        sim_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(sim_frame, text="ℹ️ Simulación de Cierre (Proyección)", font=ctk.CTkFont(weight="bold"), text_color="#1E40AF").pack(pady=5)
        
        # Buscar utilidades retenidas y efectivo
        capital = [c for c in cuentas if c.id_tipo_cuenta == 5]
        activos_corrientes = [c for c in cuentas if c.id_tipo_cuenta == 1]
        
        util_ret = next((c for c in capital if "Utilidades Retenidas" in c.nombre_cuenta), None)
        efectivo = next((c for c in activos_corrientes if "Efectivo" in c.nombre_cuenta), None)
        
        sim_text = f"La utilidad del período (${utilidad_neta:,.2f}) se sumaría a:\n"
        if util_ret:
            sim_text += f"• {util_ret.nombre_cuenta}: ${util_ret.saldo_actual:,.2f} ➔ ${(util_ret.saldo_actual + utilidad_neta):,.2f}\n"
        if efectivo:
            sim_text += f"• {efectivo.nombre_cuenta}: ${efectivo.saldo_actual:,.2f} ➔ ${(efectivo.saldo_actual + utilidad_neta):,.2f}"
            
        ctk.CTkLabel(sim_frame, text=sim_text, justify="left", text_color="#1E3A8A").pack(pady=5)
    
    def load_cuentas_tab(self):
        """Carga las cuentas del vendedor en la pestaña de Cuentas"""
        if not self.id_vendedor:
            return
        
        cuentas_tab = self.tabs["Cuentas"]
        
        # Limpiar la pestaña
        for widget in cuentas_tab.winfo_children():
            widget.destroy()
        
        # Header con título
        header_frame = ctk.CTkFrame(cuentas_tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="Mis Cuentas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#111827"
        ).pack(side="left")
        
        # Obtener cuentas del vendedor
        self.all_cuentas_vendedor = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        if not self.all_cuentas_vendedor:
            ctk.CTkLabel(
                cuentas_tab,
                text="No se encontraron cuentas",
                text_color="#6B7280"
            ).pack(pady=20)
            return
        
        # Renderizar tabla con todas las cuentas
        self.render_cuentas_table(cuentas_tab, self.all_cuentas_vendedor)
    
    def render_cuentas_table(self, parent, cuentas):
        """Renderiza la tabla de cuentas"""
        if not cuentas:
            ctk.CTkLabel(
                parent,
                text="No hay cuentas disponibles",
                text_color="#6B7280"
            ).pack(pady=20)
            return
        
        # Crear tabla de cuentas
        table_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Headers
        headers = ["Código", "Nombre", "Tipo", "Saldo", "Sistema"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="#F3F4F6")
        header_frame.pack(fill="x", pady=(0, 5))
        
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#374151",
                width=150 if i < 4 else 80
            ).grid(row=0, column=i, padx=10, pady=8, sticky="w")
        
        # Datos de cuentas
        tipos_cuenta = {
            1: "Activo Corriente",
            2: "Activo No Corriente",
            3: "Pasivo Corriente",
            4: "Pasivo No Corriente",
            5: "Capital",
            6: "Ingreso",
            7: "Gasto Operativo",
            8: "Gasto de Interés"
        }
        
        for cuenta in cuentas:
            row_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            # Código
            ctk.CTkLabel(
                row_frame,
                text=cuenta.codigo_cuenta,
                text_color="#111827",
                width=150
            ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
            # Nombre
            ctk.CTkLabel(
                row_frame,
                text=cuenta.nombre_cuenta,
                text_color="#111827",
                width=150
            ).grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            # Tipo
            ctk.CTkLabel(
                row_frame,
                text=tipos_cuenta.get(cuenta.id_tipo_cuenta, "Desconocido"),
                text_color="#6B7280",
                width=150
            ).grid(row=0, column=2, padx=10, pady=5, sticky="w")
            
            # Saldo
            ctk.CTkLabel(
                row_frame,
                text=f"${cuenta.saldo_actual:,.2f}",
                text_color="#059669" if cuenta.saldo_actual >= 0 else "#EF4444",
                width=150
            ).grid(row=0, column=3, padx=10, pady=5, sticky="w")
            
            # Sistema
            sistema_text = "✓" if cuenta.es_cuenta_de_sistema else ""
            ctk.CTkLabel(
                row_frame,
                text=sistema_text,
                text_color="#F97316",
                width=80
            ).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    
    def load_gestionar_tab(self):
        """Carga la pestaña de Agregar/Modificar Cuentas"""
        if not self.id_vendedor:
            return
        
        gestionar_tab = self.tabs["Gestionar"]
        
        # Limpiar la pestaña
        for widget in gestionar_tab.winfo_children():
            widget.destroy()
        
        # Variables de estado
        self.selected_accounts = []
        self.cuenta_widgets = {}
        self.operation_mode = ctk.StringVar(value="Modificar")
        self.increase_decrease = ctk.BooleanVar(value=True)  # True = Aumentar, False = Disminuir
        
        # Header
        header_frame = ctk.CTkFrame(gestionar_tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="Gestionar Cuentas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#111827"
        ).pack(side="left")
        
        # ComboBox para seleccionar operación
        ctk.CTkLabel(header_frame, text="Operación:", text_color="#6B7280").pack(side="left", padx=(20, 5))
        operation_combo = ctk.CTkComboBox(
            header_frame,
            values=["Agregar", "Modificar"],
            variable=self.operation_mode,
            command=self.on_operation_change,
            width=150
        )
        operation_combo.pack(side="left")
        
        # Contenedor principal scrollable
        self.main_content = ctk.CTkScrollableFrame(gestionar_tab, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Cargar vista de modificar por defecto
        self.render_modificar_view()
    
    def on_operation_change(self, choice):
        """Maneja el cambio de operación"""
        # Limpiar contenido
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        if choice == "Modificar":
            self.render_modificar_view()
        else:
            self.render_agregar_view()
    
    def render_agregar_view(self):
        """Renderiza la vista para agregar nuevas cuentas"""
        # Limpiar contenido
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
        # Contenedor principal centrado
        container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Título
        ctk.CTkLabel(
            container,
            text="➕ Agregar Nueva Cuenta",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="x", pady=10)
        
        # 1. Selección de Tipo de Cuenta
        ctk.CTkLabel(
            form_frame,
            text="Tipo de Cuenta:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        # Obtener tipos de cuenta
        from backend.DAOs.TiposCuentaDAO import TiposCuentaDAO
        tipos = TiposCuentaDAO.obtener_todos()
        
        # Formatear opciones para el combobox (Nombre - Categoria)
        opciones_tipos = []
        tipo_map = {}  # Para mapear la selección al objeto tipo
        
        for tipo in tipos:
            nombre_mostrar = f"{tipo.nombre}"
            if tipo.categoria:
                nombre_mostrar += f" - {tipo.categoria}"
            opciones_tipos.append(nombre_mostrar)
            tipo_map[nombre_mostrar] = tipo
            
        tipo_var = ctk.StringVar(value=opciones_tipos[0] if opciones_tipos else "")
        tipo_combo = ctk.CTkComboBox(
            form_frame,
            values=opciones_tipos,
            variable=tipo_var,
            width=300,
            state="readonly"
        )
        tipo_combo.pack(padx=20, pady=(0, 15), fill="x")
        
        # 2. Nombre de la Cuenta
        ctk.CTkLabel(
            form_frame,
            text="Nombre de la Cuenta:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", padx=20, pady=(5, 5))
        
        nombre_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: Caja Chica, Banco Nacional, Inventario de Ropa...",
            width=300
        )
        nombre_entry.pack(padx=20, pady=(0, 20), fill="x")
        
        # Botón Agregar
        def agregar_cuenta():
            nombre = nombre_entry.get().strip()
            if not nombre:
                self.show_error_message("El nombre de la cuenta es obligatorio")
                return
            
            # Verificar duplicados
            if CuentaDAO.verificar_nombre_duplicado(self.id_vendedor, nombre):
                self.show_error_message("Ya tienes una cuenta con este nombre")
                return
            
            # Obtener tipo seleccionado
            tipo_seleccionado = tipo_map.get(tipo_var.get())
            if not tipo_seleccionado:
                self.show_error_message("Error al seleccionar el tipo de cuenta")
                return
            
            # Generar código aleatorio
            import random
            codigo = f"{random.randint(1000, 9999)}"
            
            # Crear objeto cuenta
            from backend.models.cuentas import Cuenta
            nueva_cuenta = Cuenta(
                id=0,
                id_tipo_cuenta=tipo_seleccionado.id_tipo_cuenta,
                id_vendedor=self.id_vendedor,
                es_cuenta_plataforma=False,
                nombre_cuenta=nombre,
                codigo_cuenta=codigo,
                es_afectable=True,
                es_cuenta_de_sistema=False,
                descripcion=f"Cuenta creada por el vendedor: {nombre}",
                saldo_actual=0.0
            )
            
            # Guardar en BD
            if CuentaDAO.insertar_cuenta(nueva_cuenta):
                self.show_success_message("Cuenta agregada exitosamente")
                # Recargar pestañas
                self.load_cuentas_tab()
                # Limpiar formulario
                nombre_entry.delete(0, 'end')
            else:
                self.show_error_message("Error al guardar la cuenta")

        ctk.CTkButton(
            container,
            text="Guardar Cuenta",
            command=agregar_cuenta,
            fg_color=get_color('success'),
            hover_color="#059669",
            height=45,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=20)
    
    def render_modificar_view(self):
        """Renderiza la vista para modificar cuentas existentes"""
        self.selected_accounts = []
        self.cuenta_widgets = {}
        
        # Obtener cuentas modificables (excluir Ingresos y Gastos)
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        cuentas_modificables = [c for c in cuentas if c.id_tipo_cuenta not in [6, 7, 8]]  # Excluir Ingresos y Gastos
        
        if not cuentas_modificables:
            ctk.CTkLabel(
                self.main_content,
                text="No hay cuentas modificables",
                text_color="#6B7280"
            ).pack(pady=20)
            return
        
        # Separar cuentas por tipo
        activos = [c for c in cuentas_modificables if c.id_tipo_cuenta in [1, 2]]
        pasivos_capital = [c for c in cuentas_modificables if c.id_tipo_cuenta in [3, 4, 5]]
        
        # Instrucciones
        inst_frame = ctk.CTkFrame(self.main_content, fg_color="#EFF6FF", corner_radius=8)
        inst_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            inst_frame,
            text="📝 Selecciona DOS cuentas para realizar una transacción contable",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1E40AF"
        ).pack(pady=10, padx=15)
        
        # Contenedor de cuentas
        accounts_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        accounts_container.pack(fill="both", expand=True)
        
        # Columna de Activos
        activos_frame = ctk.CTkFrame(accounts_container, fg_color="#F9FAFB", corner_radius=8)
        activos_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            activos_frame,
            text="💰 ACTIVOS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#059669"
        ).pack(pady=10)
        
        for cuenta in activos:
            self.create_account_card(activos_frame, cuenta)
        
        # Columna de Pasivos y Capital
        pasivos_frame = ctk.CTkFrame(accounts_container, fg_color="#F9FAFB", corner_radius=8)
        pasivos_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            pasivos_frame,
            text="📊 PASIVOS Y CAPITAL",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DC2626"
        ).pack(pady=10)
        
        for cuenta in pasivos_capital:
            self.create_account_card(pasivos_frame, cuenta)
        
        # Panel de transacción (inicialmente oculto)
        self.transaction_panel = ctk.CTkFrame(self.main_content, fg_color="#FFFFFF", corner_radius=8, border_width=2, border_color="#F97316")
        self.transaction_panel.pack(fill="x", pady=(20, 0))
        self.transaction_panel.pack_forget()  # Ocultar inicialmente
    
    def create_account_card(self, parent, cuenta):
        """Crea una tarjeta de cuenta seleccionable"""
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=6, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", padx=10, pady=5)
        
        # Hacer clickeable
        card.bind("<Button-1>", lambda e: self.toggle_account_selection(cuenta, card))
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=8)
        content_frame.bind("<Button-1>", lambda e: self.toggle_account_selection(cuenta, card))
        
        # Nombre de la cuenta
        name_label = ctk.CTkLabel(
            content_frame,
            text=cuenta.nombre_cuenta,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#111827",
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        name_label.bind("<Button-1>", lambda e: self.toggle_account_selection(cuenta, card))
        
        # Indicador numérico (inicialmente oculto)
        indicator_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#F97316",
            corner_radius=12,
            width=30,
            height=30
        )
        indicator_label.pack(side="right", padx=(10, 5))
        indicator_label.pack_forget()  # Ocultar inicialmente
        
        # Saldo
        saldo_label = ctk.CTkLabel(
            content_frame,
            text=f"${cuenta.saldo_actual:,.2f}",
            font=ctk.CTkFont(size=13),
            text_color="#059669" if cuenta.saldo_actual >= 0 else "#EF4444"
        )
        saldo_label.pack(side="right")
        saldo_label.bind("<Button-1>", lambda e: self.toggle_account_selection(cuenta, card))
        
        # Guardar referencia
        self.cuenta_widgets[cuenta.id] = {"card": card, "cuenta": cuenta, "selected": False, "indicator": indicator_label}
    
    def toggle_account_selection(self, cuenta, card):
        """Maneja la selección/deselección de cuentas"""
        widget_info = self.cuenta_widgets[cuenta.id]
        
        if widget_info["selected"]:
            # Deseleccionar
            widget_info["selected"] = False
            card.configure(border_color="#E5E7EB", border_width=1)
            self.selected_accounts.remove(cuenta)
        else:
            # Verificar que no se hayan seleccionado ya 2 cuentas
            if len(self.selected_accounts) >= 2:
                return
            
            # Seleccionar
            widget_info["selected"] = True
            card.configure(border_color="#F97316", border_width=3)
            self.selected_accounts.append(cuenta)
        
        # Actualizar indicadores numéricos
        self.update_selection_indicators()
        
        # Mostrar/ocultar panel de transacción
        if len(self.selected_accounts) == 2:
            self.show_transaction_panel()
        else:
            self.transaction_panel.pack_forget()
    
    def update_selection_indicators(self):
        """Actualiza los indicadores numéricos (1, 2) en las cuentas seleccionadas"""
        # Primero, ocultar todos los indicadores
        for cuenta_id, widget_info in self.cuenta_widgets.items():
            indicator = widget_info.get("indicator")
            if indicator:
                indicator.pack_forget()
                indicator.configure(text="")
        
        # Luego, mostrar solo los de las cuentas seleccionadas
        for i, cuenta in enumerate(self.selected_accounts):
            widget_info = self.cuenta_widgets[cuenta.id]
            indicator = widget_info.get("indicator")
            if indicator:
                indicator.configure(text=str(i + 1))
                indicator.pack(side="right", padx=(10, 5), before=widget_info["card"].winfo_children()[0].winfo_children()[-1])

    
    def show_transaction_panel(self):
        """Muestra el panel de transacción cuando se seleccionan 2 cuentas"""
        # Limpiar panel
        for widget in self.transaction_panel.winfo_children():
            widget.destroy()
        
        self.transaction_panel.pack(fill="x", pady=(20, 0))
        
        cuenta1 = self.selected_accounts[0]
        cuenta2 = self.selected_accounts[1]
        
        # Título
        ctk.CTkLabel(
            self.transaction_panel,
            text="💳 Realizar Transacción",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"
        ).pack(pady=(15, 10))
        
        # Frame de entrada
        input_frame = ctk.CTkFrame(self.transaction_panel, fg_color="transparent")
        input_frame.pack(pady=10)
        
        # Monto
        ctk.CTkLabel(input_frame, text="Monto:", text_color="#6B7280").grid(row=0, column=0, padx=5, sticky="e")
        monto_entry = ctk.CTkEntry(input_frame, width=150, placeholder_text="0.00")
        monto_entry.grid(row=0, column=1, padx=5)
        
        # Switch y label dinámico
        switch_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        switch_frame.grid(row=0, column=2, padx=20)
        
        # Label que cambia según el switch
        operation_label = ctk.CTkLabel(
            switch_frame,
            text=f"Aumentar {cuenta1.nombre_cuenta}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#059669"
        )
        operation_label.pack(pady=(0, 5))
        
        def on_switch_change():
            if self.increase_decrease.get():
                operation_label.configure(text=f"Aumentar {cuenta1.nombre_cuenta}", text_color="#059669")
            else:
                operation_label.configure(text=f"Disminuir {cuenta1.nombre_cuenta}", text_color="#EF4444")
        
        switch = ctk.CTkSwitch(
            switch_frame,
            text="",
            variable=self.increase_decrease,
            command=on_switch_change,
            onvalue=True,
            offvalue=False
        )
        switch.pack()
        
        # Explicación de la lógica contable
        logic_frame = ctk.CTkFrame(self.transaction_panel, fg_color="#F3F4F6", corner_radius=6)
        logic_frame.pack(fill="x", padx=15, pady=10)
        
        # Determinar la lógica según los tipos de cuenta
        tipo1 = cuenta1.id_tipo_cuenta
        tipo2 = cuenta2.id_tipo_cuenta
        
        es_activo1 = tipo1 in [1, 2]
        es_activo2 = tipo2 in [1, 2]
        
        if es_activo1 and es_activo2:
            logic_text = "⚖️ Ambas son ACTIVOS: Si una aumenta, la otra disminuye"
        elif not es_activo1 and not es_activo2:
            logic_text = "⚖️ Ambas son PASIVOS/CAPITAL: Si una aumenta, la otra disminuye"
        else:
            logic_text = "⚖️ Una es ACTIVO y otra PASIVO/CAPITAL: Ambas aumentan o ambas disminuyen"
        
        ctk.CTkLabel(
            logic_frame,
            text=logic_text,
            font=ctk.CTkFont(size=11),
            text_color="#6B7280"
        ).pack(pady=8, padx=10)
        
        # Botón de modificar
        def realizar_transaccion():
            try:
                monto = float(monto_entry.get())
                if monto <= 0:
                    self.show_error_message("El monto debe ser mayor a 0")
                    return
                
                # Calcular montos según la lógica contable
                aumentar = self.increase_decrease.get()
                
                if es_activo1 and es_activo2:
                    # Ambos activos: uno aumenta, otro disminuye
                    monto1 = monto if aumentar else -monto
                    monto2 = -monto if aumentar else monto
                elif not es_activo1 and not es_activo2:
                    # Ambos pasivos/capital: uno aumenta, otro disminuye
                    monto1 = monto if aumentar else -monto
                    monto2 = -monto if aumentar else monto
                else:
                    # Uno activo, otro pasivo/capital: ambos en la misma dirección
                    monto1 = monto if aumentar else -monto
                    monto2 = monto if aumentar else -monto
                
                # Actualizar en la base de datos
                exito = CuentaDAO.actualizar_saldos(cuenta1.id, monto1, cuenta2.id, monto2)
                
                if exito:
                    self.show_success_message("Transacción realizada exitosamente")
                    # Recargar ambas pestañas para reflejar los cambios
                    self.load_cuentas_tab()
                    self.render_modificar_view()
                else:
                    self.show_error_message("Error al realizar la transacción")
                    
            except ValueError:
                self.show_error_message("Ingresa un monto válido")
        
        ctk.CTkButton(
            self.transaction_panel,
            text="✓ Modificar Cuentas",
            command=realizar_transaccion,
            fg_color=get_color('success'),
            hover_color="#059669",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(0, 15))
    
    def show_success_message(self, message):
        """Muestra un mensaje de éxito"""
        popup = ctk.CTkToplevel(self)
        popup.geometry("350x150")
        popup.title("Éxito")
        
        ctk.CTkLabel(
            popup,
            text="✅ " + message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_color('success')
        ).pack(pady=30)
        
        ctk.CTkButton(
            popup,
            text="Cerrar",
            command=popup.destroy,
            fg_color=get_color('accent')
        ).pack()
    
    def show_error_message(self, message):
        """Muestra un mensaje de error"""
        popup = ctk.CTkToplevel(self)
        popup.geometry("350x150")
        popup.title("Error")
        
        ctk.CTkLabel(
            popup,
            text="❌ " + message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#EF4444"
        ).pack(pady=30)
        
        ctk.CTkButton(
            popup,
            text="Cerrar",
            command=popup.destroy,
            fg_color="#6B7280"
        ).pack()

    def export_report(self):
        """Placeholder para exportar reporte"""
        print("Exportar reporte - Funcionalidad pendiente")
        
    def show_interpretations(self):
        """Placeholder para mostrar interpretaciones"""
        print("Mostrar interpretaciones - Funcionalidad pendiente")
        
    def load_proforma_tab(self):
        """Carga la pestaña de Estados Financieros Proforma"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Proforma"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        # Top Frame para Configuración
        config_frame = ctk.CTkFrame(tab, fg_color="transparent")
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="Proyección Financiera (Proforma)",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(side="left")
        
        # Switch Modo
        self.proforma_mode = ctk.StringVar(value="pct") # 'pct' or 'amount'
        
        def toggle_mode():
            mode = self.proforma_mode.get()
            # Actualizar etiquetas de entradas
            for cuenta_id, widgets in self.proforma_entries.items():
                label = widgets["label"]
                nombre = widgets["nombre"]
                if mode == "amount":
                    label.configure(text=f"Nuevo Monto {nombre} ($)")
                else:
                    label.configure(text=f"Crecimiento {nombre} (%)")
        
        switch_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        switch_frame.pack(side="right")
        
        ctk.CTkSwitch(
            switch_frame, 
            text="Modo: Monto ($)", 
            variable=self.proforma_mode, 
            onvalue="amount", 
            offvalue="pct", 
            command=toggle_mode
        ).pack(side="right", padx=10)
        
        ctk.CTkLabel(switch_frame, text="Modo: Porcentaje (%)", text_color="#374151").pack(side="right")
        
        # Frame Principal (Scrollable)
        main_scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # --- SECCIÓN DE ENTRADAS ---
        inputs_frame = ctk.CTkFrame(main_scroll, fg_color="#FFFFFF", corner_radius=8)
        inputs_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(inputs_frame, text="Configurar Proyección de Resultados", font=ctk.CTkFont(weight="bold"), text_color="#4B5563").pack(anchor="w", padx=15, pady=10)
        
        # Obtener cuentas de resultados
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        resultados_cuentas = [c for c in cuentas if c.id_tipo_cuenta in [6, 7]] # Ingresos y Gastos
        
        self.proforma_entries = {}
        
        # Grid de entradas
        grid_frame = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i, cuenta in enumerate(resultados_cuentas):
            row = i // 2
            col = i % 2
            
            f = ctk.CTkFrame(grid_frame, fg_color="transparent")
            f.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            lbl_text = f"Crecimiento {cuenta.nombre_cuenta} (%)"
            lbl = ctk.CTkLabel(f, text=lbl_text, font=ctk.CTkFont(size=12), anchor="w")
            lbl.pack(fill="x")
            
            entry = ctk.CTkEntry(f, placeholder_text="0.0")
            entry.pack(fill="x")
            
            self.proforma_entries[cuenta.id] = {"entry": entry, "label": lbl, "nombre": cuenta.nombre_cuenta, "cuenta": cuenta}
            
        # Botón Generar
        ctk.CTkButton(
            inputs_frame,
            text="Generar Proforma",
            command=self.apply_proforma,
            fg_color=get_color('accent'),
            height=40,
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=15)
        
        # --- SECCIÓN DE RESULTADOS ---
        self.proforma_results_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        self.proforma_results_frame.pack(fill="both", expand=True, pady=10)
        
    def apply_proforma(self):
        """Calcula y muestra los estados proforma"""
        mode = self.proforma_mode.get()
        
        # Leer entradas
        inputs = {}
        for cid, widgets in self.proforma_entries.items():
            val_str = widgets["entry"].get().strip()
            try:
                val = float(val_str) if val_str else 0.0
            except ValueError:
                val = 0.0
            inputs[cid] = val
            
        # Obtener datos actuales
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        # 1. PROYECTAR ESTADO DE RESULTADOS
        is_data = []
        total_ingresos_proj = 0.0
        total_gastos_proj = 0.0
        
        for cuenta in cuentas:
            if cuenta.id_tipo_cuenta in [6, 7, 8]: # Resultados
                val_actual = float(cuenta.saldo_actual)
                new_val = val_actual
                
                # Aplicar proyección si hay entrada
                if cuenta.id in inputs:
                    input_val = inputs[cuenta.id]
                    if mode == "pct":
                        new_val = val_actual * (1.0 + input_val / 100.0)
                    else:
                        # Si es monto, y el input es 0 y estaba vacío, mantenemos actual. Si puso 0 explícito, es 0.
                        # Aquí simplificamos: si input != 0 o el texto no está vacío, usamos input.
                        entry_text = self.proforma_entries[cuenta.id]["entry"].get().strip()
                        if entry_text != "":
                            new_val = input_val
                        # Si está vacío, new_val sigue siendo val_actual
                
                if cuenta.id_tipo_cuenta == 6:
                    total_ingresos_proj += new_val
                elif cuenta.id_tipo_cuenta in [7, 8]:
                    total_gastos_proj += new_val
                    
                is_data.append({"Cuenta": cuenta.nombre_cuenta, "Monto": new_val, "TipoId": cuenta.id_tipo_cuenta})
        
        # Calcular Utilidad e Impuestos Proyectados
        utilidad_antes_ir = total_ingresos_proj - total_gastos_proj
        
        vendedor = VendedorDAO.obtener_por_id_usuario(self.usuario.id)
        ir_proj = 0.0
        if vendedor and vendedor.es_contribuyente and utilidad_antes_ir > 0:
            ir_proj = utilidad_antes_ir * 0.30
            
        utilidad_neta_proj = utilidad_antes_ir - ir_proj
        
        # Agregar filas de totales a IS Data
        is_data.append({"Cuenta": "Utilidad Antes de Impuestos", "Monto": utilidad_antes_ir, "TipoId": 99})
        is_data.append({"Cuenta": "Impuestos (30%)", "Monto": ir_proj, "TipoId": 99})
        is_data.append({"Cuenta": "Utilidad Neta Proyectada", "Monto": utilidad_neta_proj, "TipoId": 99})
        
        # 2. PROYECTAR BALANCE GENERAL
        bs_data = []
        
        # Lógica simplificada:
        # Activos: Efectivo aumenta por la Utilidad Neta
        # Pasivos: Constantes
        # Capital: Utilidades Retenidas aumenta por la Utilidad Neta
        
        for cuenta in cuentas:
            if cuenta.id_tipo_cuenta in [1, 2, 3, 4, 5]: # Balance
                val_actual = float(cuenta.saldo_actual)
                new_val = val_actual
                nombre_lower = cuenta.nombre_cuenta.lower()
                
                # Ajuste Activo (Efectivo)
                if cuenta.id_tipo_cuenta == 1 and ("efectivo" in nombre_lower or "banco" in nombre_lower or "caja" in nombre_lower):
                    new_val += utilidad_neta_proj
                
                # Ajuste Capital (Utilidades Retenidas)
                if cuenta.id_tipo_cuenta == 5 and ("utilidades retenidas" in nombre_lower or "resultados acumulados" in nombre_lower):
                    new_val += utilidad_neta_proj
                
                # Si no encuentra cuentas específicas, podría desbalancearse. 
                # En un sistema real, se cuadraría contra una cuenta "plug".
                # Aquí asumimos que el usuario tiene estas cuentas o el desbalance se mostrará.
                
                bs_data.append({"Cuenta": cuenta.nombre_cuenta, "Monto": new_val, "TipoId": cuenta.id_tipo_cuenta})
                
        # --- RENDERIZAR RESULTADOS ---
        for w in self.proforma_results_frame.winfo_children():
            w.destroy()
            
        # Contenedor lado a lado
        tables_container = ctk.CTkFrame(self.proforma_results_frame, fg_color="transparent")
        tables_container.pack(fill="x", expand=True)
        
        # Helper tabla
        def render_table(parent, title, data, total_base_vert):
            frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=8)
            frame.pack(side="left", fill="both", expand=True, padx=5)
            
            ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold", size=14), text_color="#111827").pack(pady=10)
            
            # Headers
            h_frame = ctk.CTkFrame(frame, fg_color="#F3F4F6")
            h_frame.pack(fill="x")
            ctk.CTkLabel(h_frame, text="Cuenta", font=ctk.CTkFont(weight="bold", size=11), width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(h_frame, text="Monto Proy.", font=ctk.CTkFont(weight="bold", size=11), width=100, anchor="e").pack(side="right", padx=5)
            ctk.CTkLabel(h_frame, text="Vert %", font=ctk.CTkFont(weight="bold", size=11), width=60, anchor="e").pack(side="right", padx=5)
            
            scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent", height=300)
            scroll.pack(fill="both", expand=True)
            
            for item in data:
                row = ctk.CTkFrame(scroll, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                monto = item["Monto"]
                vert = (monto / total_base_vert * 100) if total_base_vert else 0.0
                
                font = ctk.CTkFont(weight="bold" if item.get("TipoId") == 99 else "normal", size=12)
                
                ctk.CTkLabel(row, text=item["Cuenta"], font=font, width=150, anchor="w").pack(side="left", padx=5)
                ctk.CTkLabel(row, text=f"${monto:,.2f}", font=font, width=100, anchor="e").pack(side="right", padx=5)
                ctk.CTkLabel(row, text=f"{vert:.1f}%", font=font, width=60, anchor="e", text_color="#6B7280").pack(side="right", padx=5)

        # Totales para vertical
        total_activos_proj = sum(d["Monto"] for d in bs_data if d["TipoId"] in [1, 2])
        
        render_table(tables_container, "Balance General Proforma", bs_data, total_activos_proj)
        render_table(tables_container, "Estado de Resultados Proforma", is_data, total_ingresos_proj)
        
        # Resumen Final
        summary = ctk.CTkFrame(self.proforma_results_frame, fg_color="#EFF6FF", corner_radius=8)
        summary.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            summary, 
            text=f"💡 La Utilidad Neta Proyectada de ${utilidad_neta_proj:,.2f} se ha capitalizado en el Balance General (Efectivo y Utilidades Retenidas).",
            text_color="#1E40AF",
            font=ctk.CTkFont(size=12)
        ).pack(pady=10)

    def load_graficos_tab(self):
        """Carga la pestaña de Gráficos Financieros"""
        if not self.id_vendedor:
            return
            
        tab = self.tabs["Graficos"]
        for widget in tab.winfo_children():
            widget.destroy()
            
        # Scrollable Frame Principal
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            scroll_frame,
            text="Análisis Gráfico Financiero",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#111827"
        ).pack(pady=(0, 20))
        
        # --- OBTENCIÓN DE DATOS ---
        cuentas = CuentaDAO.obtener_por_id_vendedor(self.id_vendedor)
        
        activos_data = {}
        pasivos_capital_data = {}
        
        total_activos = 0.0
        total_pasivo_capital = 0.0
        
        for c in cuentas:
            val = float(c.saldo_actual)
            if c.id_tipo_cuenta in [1, 2]: # Activos
                activos_data[c.nombre_cuenta] = val
                total_activos += val
            elif c.id_tipo_cuenta in [3, 4, 5]: # Pasivos y Capital
                pasivos_capital_data[c.nombre_cuenta] = val
                total_pasivo_capital += val
                
        # --- GRÁFICOS DE PASTEL (Composición) ---
        pie_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        pie_frame.pack(fill="x", pady=(0, 20))
        
        # Helper para crear gráfico de pastel
        def create_pie_chart(parent, data, total, title):
            fig, ax = plt.subplots(figsize=(5, 5.5))
            
            if data and total > 0:
                # Filtrar valores pequeños (< 3%)
                threshold = total * 0.03
                main_items = {}
                otros_total = 0.0
                
                for name, val in data.items():
                    if val >= threshold:
                        main_items[name] = val
                    else:
                        otros_total += val
                
                if otros_total > 0:
                    main_items['Otros'] = otros_total
                    
                labels = list(main_items.keys())
                sizes = list(main_items.values())
                colors = plt.cm.Set3(range(len(labels)))
                
                wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=colors)
                
                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(9)
                    
                ax.legend(wedges, labels, title="Cuentas", loc="upper center", bbox_to_anchor=(0.5, -0.05), fontsize=8, ncol=2)
                ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
            else:
                ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
                ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
                
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10)
            
        create_pie_chart(pie_frame, activos_data, total_activos, "Composición de Activos")
        create_pie_chart(pie_frame, pasivos_capital_data, total_pasivo_capital, "Composición Pasivo + Capital")
        
        # --- GRÁFICO DE BARRAS (Comparación Activos) ---
        bar_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        bar_frame.pack(fill="x", pady=10)
        
        fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
        
        periods = ['Período Anterior', 'Período Actual']
        values = [0.0, total_activos] # Anterior asumido en 0
        colors = ['#E5E7EB', '#06B6D4']
        
        bars = ax_bar.bar(periods, values, color=colors, width=0.5)
        ax_bar.set_title('Crecimiento de Activos Totales', fontsize=14, fontweight='bold')
        ax_bar.set_ylabel('Monto ($)', fontsize=12)
        
        # Etiquetas de valor
        for bar in bars:
            height = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.2f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
                    
        ax_bar.grid(axis='y', alpha=0.3)
        
        canvas_bar = FigureCanvasTkAgg(fig_bar, master=bar_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(fill="x", padx=20)
