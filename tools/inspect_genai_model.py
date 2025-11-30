import inspect
import google.generativeai as genai
GM = genai.GenerativeModel
print('GenerativeModel doc:', GM.__doc__[:400])
print('\nMethods:')
print([m for m in dir(GM) if not m.startswith('_')])
# show signature of generate_* methods
for m in ['generate_content','generate','generate_text','generate_sync']:
    if hasattr(GM, m):
        fn = getattr(GM, m)
        try:
            print('\nSignature for', m, inspect.signature(fn))
        except Exception as e:
            print('\nCould not get signature for', m, e)
