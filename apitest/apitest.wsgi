import os, sys

# ensures my project is in my path

path1 = '/home/delane/UW/Python/UWPython/Python2'
path2 = '/home/delane/UW/Python/UWPython/Python2/apitest'
sys.path.insert(0, path1)
sys.path.insert(1, path2)
os.environ['DJANGO_SETTINGS_MODULE'] = 'apitest.settings'

# This has to be done here so that django will be in a directory that's in the python path
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()