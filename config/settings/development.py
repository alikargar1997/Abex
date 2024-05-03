from .base import *

DEBUG = env.bool("DEBUG", True)

SECRET_KEY = env.str(
    "SECRET_KEY", "django-insecure-yz3ek5cwf)6*o@s1#qk59$cb$p&w*mc^17$23d#0loo41u$bo@"
)

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


