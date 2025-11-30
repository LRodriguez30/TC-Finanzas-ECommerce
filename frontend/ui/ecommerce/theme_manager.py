"""Manejador simple de paletas de colores para la app.

Proporciona paletas y funciones para obtener colores por clave.
"""
PALETTES = {
    'Minimal': {
        'bg': '#FFFFFF',
        'text': '#111827',
        'muted': '#6B7280',
        'primary': '#06B6D4',
        'accent': '#06B6D4',
        'success': '#10B981',
        'card_bg': '#FAFAFA'
    },
    'Ocean': {
        'bg': '#F0FAFF',
        'text': '#0F172A',
        'muted': '#475569',
        'primary': '#0EA5A4',
        'accent': '#0284C7',
        'success': '#06B6D4',
        'card_bg': '#F8FDFF'
    },
    'Warm': {
        'bg': '#FFFBF0',
        'text': '#1F2937',
        'muted': '#6B4F2A',
        'primary': '#F97316',
        'accent': '#F97316',
        'success': '#65A30D',
        'card_bg': '#FFF7ED'
    }
}

_current = PALETTES['Minimal']

def set_palette(name: str):
    global _current
    if name in PALETTES:
        _current = PALETTES[name]
        return True
    return False

def get_color(key: str):
    return _current.get(key)

def available_palettes():
    return list(PALETTES.keys())
