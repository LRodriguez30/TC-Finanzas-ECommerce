import os
import traceback
try:
    import google.generativeai as genai
except Exception as e:
    print('No se pudo importar google.generativeai:', e)
    raise SystemExit(1)

API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GEN_API_KEY')
if not API_KEY:
    print('No hay API Key en GEMINI_API_KEY o GEN_API_KEY. Ponla y vuelve a ejecutar.')
    raise SystemExit(1)

print('Usando API Key desde variable de entorno')
try:
    genai.configure(api_key=API_KEY)
    print('genai configured OK')
    models = genai.list_models()
    print('Tipo de retorno de list_models():', type(models))
    try:
        # Imprimir representación completa (truncada)
        import pprint
        pprint.pprint(models)
    except Exception:
        print('No se pudo pprint models; repr:')
        print(repr(models)[:4000])
    # Si es iterable, intentar mostrar atributos claves
    try:
        cnt = 0
        for m in models:
            print('\n---- Modelo', cnt, '----')
            try:
                print('name:', getattr(m, 'name', None))
                print('display_name:', getattr(m, 'display_name', None))
                print('supports:', getattr(m, 'supported_methods', None))
            except Exception:
                print('model repr:', repr(m)[:1000])
            cnt += 1
            if cnt >= 50:
                break
        if cnt == 0:
            print('No se listaron modelos (iterable vacío).')
    except Exception as e:
        print('No se pudo iterar sobre models:', e)
except Exception:
    print('Error al llamar list_models:')
    traceback.print_exc()
    raise SystemExit(2)
