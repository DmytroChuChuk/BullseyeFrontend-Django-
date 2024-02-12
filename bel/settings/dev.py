from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=vsgdb9e-6_k5!u59%@q3y4r^26s@r)umnvaq%r4%6&0on@f7#"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



try:
    from .local import *
except ImportError:
    pass
