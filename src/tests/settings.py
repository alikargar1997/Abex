from config.settings.base import *

SECRET_KEY = "django-insecure-test-key"

DATABASES = {
    "default": env.db(
        default="mysql://abex:supersecretpassword@127.0.0.1:3306/abex"
    ),
}
