import google.generativeai as genai
print('genai module attrs:')
print([a for a in dir(genai) if not a.startswith('_')])
# Try to inspect classes
for name in ['GenerativeModel','generate_text','generate','generate_text_stream','TextGeneration']:
    if hasattr(genai, name):
        print('\nFound', name, '->', getattr(genai, name))
