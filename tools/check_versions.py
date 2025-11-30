import sys
import importlib
import requests

print('Python', sys.version)
importlib.invalidate_caches()
try:
    import google.generativeai as genai
    print('google.generativeai imported, version=', getattr(genai, '__version__', 'no __version__'))
except Exception as e:
    print('google.generativeai import error:', e)

print('requests', requests.__version__)
