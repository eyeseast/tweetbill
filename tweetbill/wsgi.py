import os, sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
APPS_PATH = os.path.join(PROJECT_ROOT, 'apps')
sys.path.insert(0, APPS_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tweetbill.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
