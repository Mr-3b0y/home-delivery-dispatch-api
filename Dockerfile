# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Variables de entorno recomendadas y anulación de proxy
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROXY_HTTP="" \
    PROXY_HTTPS="" \
    http_proxy="" \
    https_proxy="" \
    HTTP_PROXY="" \
    HTTPS_PROXY="" \
    no_proxy="localhost,127.0.0.1" \
    NO_PROXY="localhost,127.0.0.1"

# Define directorio de trabajo
WORKDIR /app

# Copiamos primero solo el directorio de requisitos
COPY requirements/ /app/requirements/

# Instala dependencias Python
RUN pip install --upgrade pip 
RUN pip install -r /app/requirements/all.txt

# Copia el resto del proyecto
COPY . /app/

# Hacer el script de entrada ejecutable
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto 8000 para el servidor
EXPOSE 8000

# Usar el script de entrada como punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]