from decouple import config
from datetime import timedelta

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e$ixd@itgm3)5nnctoohj&+k(%l5!dv*nqg$*$h2m*e6n#kcsf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}