EVALUACIÓN SUMATIVA 4 - INSTRUCCIONES DE DEPLOY EN PYTHONANYWHERE

PARTE 1: REQUERIMIENTOS Y PREPARACIÓN

1. Código Fuente: Se debe clonar el repositorio de github

2. Dependencias: Se tiene que tener un archivo requirements hecho para instalar todas las librerias necesarias para el funcionamiento del proyecto: pip freeze > requirements.txt

PARTE 2: CONFIGURACIÓN DE PYTHONANYWHERE (Consola Bash)

1.  **Entorno Virtual (venv):**
a. Se crea el entorno virtual de python (mkvirtualenv --python=/usr/bin/python3.12 venv)
b. Se instalan dependencias (pip install -r /home/crelatentt/EVA3-BACKEND-BRACAMONTE/requirements.txt)

PARTE 3: AJUSTES CRÍTICOS EN settings.py
SE MODIFICAN ESTAS COSAS EN SETTINGS, SI NO SE MODIFICAN LA PAGINA NO FUNCIONARÁ

1. settings.py (DEBUG = False) 

2. Hosts Permitidos: ALLOWED_HOSTS = ['crelatentt.pythonanywhere.com']
MEDIA_URL = '/' # CRÍTICO: Usar '/' evitando la duplicidad '/media/media/' en las URL de las fotos (ESTO ES PARA QUE CARGUEN)
MEDIA_ROOT = MEDIA_DIR
	
PARTE 4: CONFIGURACIÓN WSGI (para solucionar ModuleNotFoundError)

import os
import sys

La ruta tiene que estar en la carpeta donde está el proyecto base
path = os.path.expanduser('~/EVA3-BACKEND-BRACAMONTE')
if path not in sys.path:
    sys.path.insert(0, path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'PRUEBA3BACKEND.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

application = StaticFilesHandler(get_wsgi_application())
