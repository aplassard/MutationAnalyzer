import os
default_settings = 'production_settings'
settings = os.getenv('DJANGO_SETTINGS_MODULE',default_settings)
if settings != default_settings:
    from local_settings import *
else:
    from production_settings import *

