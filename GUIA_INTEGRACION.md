# Guía de Integración y Uso: TC-Finanzas-ECommerce

Este documento detalla la integración completa del módulo de **E-commerce y Análisis Financiero** (desarrollado en Python/CustomTkinter) dentro del proyecto `TC-Finanzas-ECommerce`.

---

## 📋 Resumen de la Integración

Se fusionó exitosamente el prototipo de E-commerce dentro de `TC-Finanzas-ECommerce`. El flujo de usuario es:

1. **Login** → Sistema de autenticación original
2. **Dashboard Principal** → Módulo `EcommerceApp` con navegación completa

---

## 🔧 Archivos Modificados del Proyecto Destino

### `frontend/ui/pagina_principal.py`
**Cambios realizados:**
- Reemplazó contenido original (etiquetas simples) por instanciación de `EcommerceApp`
- Agregó redimensionamiento automático de ventana a 1200x800
- Configuró límites de tamaño (min: 1000x600, max: 2000x1500)
- Habilitó redimensionamiento manual

**Propósito:** Punto de entrada al dashboard tras autenticación exitosa.

### `requirements.txt`
**Dependencias agregadas:**
- `matplotlib` - Gráficos financieros
- `pandas` - Procesamiento de datos
- `openpyxl` - Lectura de Excel
- `xlsxwriter` - Escritura de Excel

---

## 📁 Estructura de Archivos Nuevos

### Frontend: `frontend/ui/ecommerce/`

| Archivo | Descripción |
|---------|-------------|
| `__init__.py` | Inicializador del paquete |
| `app.py` | Clase principal `EcommerceApp` - Gestiona navegación |
| `sidebar.py` | Barra lateral con menú de navegación |
| `data.py` | Datos mock (productos y ratios financieros) |

#### Subdirectorio: `pages/`

| Archivo | Funcionalidad |
|---------|---------------|
| `home.py` | Página de bienvenida |
| `products.py` | Catálogo con búsqueda y filtros de precio |
| `financial.py` | Análisis financiero avanzado (Balance, Ratios, Gráficos) |
| `sellers.py` | Formulario de registro de vendedores |

### Backend: `backend/logic/`

| Archivo | Propósito |
|---------|-----------|
| `__init__.py` | Inicializador del paquete |
| `financial_models.py` | Análisis vertical, horizontal, ratios |
| `excel_handler.py` | Generación de plantillas y carga de datos Excel |

---

## 🎨 Paleta de Colores Aplicada

| Elemento | Color | Código Hex |
|----------|-------|------------|
| Sidebar | Verde Oliva | `#65A30D` |
| Hover Sidebar | Naranja | `#F97316` |
| Botones Principales | Naranja | `#F97316` |
| Botón Exportar | Verde | `#65A30D` |
| Textos Énfasis | Marrón Tierra | `#854D0E` |
| Fondos Inputs | Gris Claro | `#D1D5DB` |

---

## ✅ Funcionalidades Implementadas

### 1. **Productos**
- Visualización en tarjetas (3 columnas)
- Búsqueda en tiempo real
- Filtro por rango de precio (slider)
- Botón "Añadir" por producto

### 2. **Vendedores**
- Formulario completo de registro
- Carga de logo (selector de archivos)
- Contador de palabras en descripción
- Validación de campos obligatorios
- Persistencia en `sellers.json`
- Mensajes de éxito/error

### 3. **Análisis Financiero**
- **Plantillas Excel:** Descarga de `Plantilla_Financiera.xlsx`
- **Importación:** Carga de datos de año base y actual
- **Pestañas:**
  - Balance General
  - Estado de Resultados
  - Origen y Aplicación
  - Razones Financieras
  - Gráficos (matplotlib integrado)

### 4. **Navegación**
- Sidebar persistente con 5 secciones
- Transiciones fluidas entre vistas
- Botón de cerrar sesión

---

## 🚀 Instrucciones de Uso

### Instalación
```bash
cd TC-Finanzas-ECommerce
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

### Flujo de Prueba
1. **Login:** Ingrese credenciales válidas o regístrese
2. **Inicio:** Verá mensaje de bienvenida
3. **Productos:** Pruebe búsqueda y filtros
4. **Vendedores:** Complete formulario y registre
5. **Financiero:** Descargue plantilla → Complete datos → Importe

---

## 🐛 Correcciones Aplicadas

### Error 1: `AttributeError: 'SellersPage' object has no attribute 'update_word_count'`
**Solución:** Agregado método `update_word_count()` en `sellers.py` líneas 89-93

### Error 2: Ventana muy pequeña (800x400)
**Solución:** Redimensionamiento automático a 1200x800 en `pagina_principal.py`

### Error 3: Imports incorrectos
**Solución:** Actualizados imports absolutos:
- `products.py`: `from frontend.ui.ecommerce.data import MOCK_PRODUCTS`
- `financial.py`: `from backend.logic.financial_models import FinancialAnalyzer`

---

## 📂 Mapa de Archivos Clave

```
TC-Finanzas-ECommerce/
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias (MODIFICADO)
├── frontend/
│   ├── ui/
│   │   ├── pagina_principal.py      # Puente Login→Dashboard (MODIFICADO)
│   │   └── ecommerce/               # NUEVO MÓDULO
│   │       ├── app.py               # Contenedor principal
│   │       ├── sidebar.py           # Navegación lateral
│   │       ├── data.py              # Datos mock
│   │       └── pages/
│   │           ├── home.py
│   │           ├── products.py
│   │           ├── financial.py
│   │           └── sellers.py
└── backend/
    └── logic/                       # NUEVA LÓGICA
        ├── financial_models.py
        └── excel_handler.py
```

---

## 📝 Notas Importantes

- **Persistencia:** Los vendedores se guardan en `sellers.json` en la raíz del proyecto
- **Excel:** Las plantillas se generan en la carpeta seleccionada por el usuario
- **Autenticación:** Sigue usando el sistema original de `TC-Finanzas-ECommerce`
- **Ventana:** Se redimensiona automáticamente al entrar al dashboard
