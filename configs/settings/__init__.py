from .base import *
from decouple import config

if config("ENV", default=None) == 'production':
    from .production import *
elif config("ENV", default=None) == 'development':
    from .dev import *
elif config("ENV", default=None) == 'testing':
    from .testing import *
else:
    raise ValueError("ENV variable is not set or is invalid. Please set it to 'production', 'development', or 'testing'.")