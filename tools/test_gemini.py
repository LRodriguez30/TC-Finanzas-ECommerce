import os
import json
import traceback

# Intentará tomar la API key desde el propio chatbot.py (constante) si existe,
# de lo contrario desde la variable de entorno GEMINI_API_KEY o GEN_API_KEY.
try:
    from frontend.ui.ecommerce.pages.chatbot import API_KEY as FILE_API_KEY
except Exception:
    FILE_API_KEY = ''

API_KEY = FILE_API_KEY or os.environ.get('GEMINI_API_KEY') or os.environ.get('GEN_API_KEY')

if not API_KEY:
    print('No se encontró API Key. Pegue su API Key en frontend/ui/ecommerce/pages/chatbot.py en la constante API_KEY o exporte GEMINI_API_KEY.')
    raise SystemExit(1)

print('Usando API Key desde', 'archivo' if FILE_API_KEY else 'variable de entorno')

# Intentar usar la librería oficial `google.generativeai` para diagnósticos más fiables
try:
    import google.generativeai as genai
    print('google.generativeai detectado, versión:', getattr(genai, '__version__', 'desconocida'))
    genai.configure(api_key=API_KEY)

    # Primero, listar modelos disponibles (esto también verifica permisos y alcance)
    try:
        models = genai.list_models()
        print('Lista de modelos (primeros 20, si hay):')
        for m in (models[:20] if isinstance(models, list) else []):
            try:
                # model puede ser un dict o un objeto; imprimir identificador razonable
                print(' -', getattr(m, 'name', repr(m)))
            except Exception:
                print(' -', m)
    except Exception as e:
        print('Error al listar modelos (suele indicar permiso/endpoint/billing):')
        traceback.print_exc()

    # Probar una generación simple usando modelos que suelen estar disponibles.
    # Basado en list_models, preferimos los nombres en formato 'models/...' que devuelve la API.
    model_candidates = [
        'models/gemini-pro-latest',
        'models/gemini-flash-latest',
        'models/gemini-2.5-flash',
        'models/gemini-2.5-pro',
        'models/gemini-2.0-flash',
        'models/text-bison-001',
    ]
    last_exc = None
    for mc in model_candidates:
        try:
            print('\nProbando generación con modelo:', mc)
            model = genai.GenerativeModel(model_name=mc)
            # generate_content espera una lista/estructura de contenidos.
            # La estructura esperada es un Content con 'parts', cada 'part' puede tener 'text'.
            resp = model.generate_content([{'parts': [{'text': 'Prueba corta: di Hola'}]}])
            print('Respuesta recibida (repr):')
            print(repr(resp)[:2000])
            # Intentar sacar texto si existe
            text = None
            try:
                # Muchas respuestas tienen .candidates o .output
                if hasattr(resp, 'text'):
                    text = getattr(resp, 'text')
                elif hasattr(resp, 'candidates'):
                    cand = getattr(resp, 'candidates')
                    if cand:
                        text = getattr(cand[0], 'content', None) or repr(cand[0])
                elif hasattr(resp, 'output'):
                    out = getattr(resp, 'output')
                    text = str(out)
            except Exception:
                pass
            if text:
                print('\nTexto extraído (truncado 2000 chars):')
                print(str(text)[:2000])
            print('Generación avanzada: OK')
            raise SystemExit(0)
        except Exception as e:
            print('Error en modelo', mc, ':', e)
            traceback.print_exc()
            last_exc = e

    print('\nNingún modelo candidato respondió correctamente. Último error:')
    traceback.print_exception(type(last_exc), last_exc, last_exc.__traceback__ if last_exc else None)
    raise SystemExit(2)

except Exception as client_exc:
    # Si falla la librería o falla por permisos, mostrar detalles y como fallback hacer una llamada REST
    print('Fallo al usar la librería `google.generativeai` o en la verificación. Detalle:')
    traceback.print_exc()
    print('\nIntentando llamada REST directa (fallback) para obtener más diagnóstico...')
    try:
        import requests
        # Uso explícito de v1beta2 por compatibilidad; si falla, pruebe v1
        urls_to_try = [
            'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generate',
            'https://generativelanguage.googleapis.com/v1/models/text-bison-001:generate'
        ]
        body = {'prompt': {'text': 'Prueba corta: di Hola'}, 'temperature': 0.2, 'maxOutputTokens': 64}
        for url in urls_to_try:
            try:
                print('Probando URL REST:', url)
                resp = requests.post(url + f'?key={API_KEY}', headers={'Content-Type': 'application/json'}, data=json.dumps(body), timeout=20)
                print('HTTP status:', resp.status_code)
                print('Response headers:', resp.headers)
                text = resp.text
                print('Body (truncado 2000 chars):')
                print(text[:2000])
            except Exception as e:
                print('Error durante request REST a', url, ':', e)
    except Exception as e:
        print('No se pudo ejecutar fallback REST:', e)
    raise SystemExit(2)
