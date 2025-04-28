#!/bin/bash

# Aplicar migraciones al iniciar el contenedor
echo "Aplicando migraciones..."
python3 manage.py migrate

# Crear superusuario si no existe
echo "Creando superusuario..."
python3 manage.py create_superuser

echo "Creando data de prueba..."
python3 manage.py load_test_data

# Iniciar el servidor usando uvicorn como estaba definido en el Dockerfile
echo "Iniciando servidor..."
exec uvicorn configs.asgi:application --host 0.0.0.0 --port 8000