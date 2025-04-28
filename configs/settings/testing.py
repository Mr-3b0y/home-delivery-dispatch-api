from decouple import config

# Use a faster test runner if available
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Patrones para descubrir archivos de prueba
TEST_DISCOVER_PATTERNS = ["test_*.py", "*_test.py", "tests.py"]

# También puedes especificar directorios específicos para las pruebas
TEST_DISCOVER_TOP_LEVEL = 'tests'

# Turn off debug for testing
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')

# Use a faster password hasher for testing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]