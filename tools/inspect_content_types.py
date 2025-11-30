import google.generativeai as genai
from google.generativeai.types import content_types
import inspect
print('content_types members:\n', [m for m in dir(content_types) if not m.startswith('_')])
print('\nDoc of to_contents:')
print(content_types.to_contents.__doc__)
try:
    print('\nExample of PARTS format from module:')
    if hasattr(content_types, 'Part'):
        print('Part class:', content_types.Part)
except Exception as e:
    print('No Part example:', e)
