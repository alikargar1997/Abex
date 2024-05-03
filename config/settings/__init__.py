import os

app_env = os.environ.get("APP_ENV", None)

if app_env == "PRODUCTION":
    from .production import *
elif app_env == "DEVELOPMENT":
    from .development import *
else:
    try:
        from .local import *
    except:
        from .base import *
