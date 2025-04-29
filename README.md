# API para Asignación de Servicios de Domicilio

Sistema de gestión de reparto a domicilio que permite la asignación de servicios entre clientes y conductores.

## Descripción General

Este proyecto es una API RESTful desarrollada con Django y Django REST Framework para gestionar un sistema de reparto a domicilio. La aplicación permite a los usuarios registrarse, gestionar direcciones, solicitar servicios de entrega y asignar conductores disponibles para realizar estos servicios.

## Proyecto Técnico para alfred.co

Este proyecto fue desarrollado como parte de un ejercicio técnico para Alfred.co, demostrando capacidades en el diseño e implementación de APIs RESTful escalables para la gestión de servicios de entrega a domicilio.

### Objetivos del Ejercicio

- Diseñar una arquitectura robusta para un sistema de asignación de servicios
- Implementar autenticación segura y gestión de usuarios
- Desarrollar lógica de negocio para la asignación óptima de conductores
- Construir una API documentada y fácilmente consumible por clientes frontend

## Características Principales

- **Gestión de usuarios**: Registro, autenticación y perfiles de usuario
- **Gestión de conductores**: Registro de conductores con información de vehículos y ubicación en tiempo real
- **Gestión de direcciones**: Almacenamiento y gestión de direcciones de clientes
- **Gestión de servicios**: Creación y seguimiento de servicios de entrega
- **Autenticación JWT**: Autenticación segura mediante tokens JWT

## Tecnologías Utilizadas

- **Backend**: Django 5.2, Django REST Framework
- **Base de datos**: PostgreSQL
- **Contenedorización**: Docker y Docker Compose
- **Documentación de API**: drf-spectacular (OpenAPI/Swagger)
- **Autenticación**: Simple JWT

## Requisitos Previos

- Docker y Docker Compose
- Git

## Estructura del Proyecto

El proyecto sigue una arquitectura modular basada en aplicaciones Django:

- **users**: Gestión de usuarios y autenticación
- **drivers**: Gestión de conductores
- **addresses**: Gestión de direcciones
- **services**: Gestión de servicios de entrega
- **core**: Funcionalidades centrales y utilidades
- **authentication**: Autenticación personalizada
- **common**: Componentes reutilizables

## Instalación y Configuración

### Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone https://github.com/Mr-3b0y/home-delivery-dispatch-api.git
cd home-delivery-dispatch-api
```

2. Crear archivo .env a partir del ejemplo:
```bash
cp .env.example .env
```

3. Editar el archivo .env con tus propias configuraciones:
```
ENV=development
SECRET_KEY=tu-clave-secreta-personalizada
DEBUG=True
DB_NAME=homedelivery
DB_USER=postgres
DB_PASSWORD=tu-contraseña
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@ejemplo.com
DJANGO_SUPERUSER_PASSWORD=admin
```

### Ejecución con Docker Compose

1. Construir e iniciar los contenedores:
```bash
docker-compose up -d
```

2. La API estará disponible en: http://localhost:8000/

### Acceso a la Documentación de API

La documentación interactiva de la API está disponible en:

- Swagger UI: http://localhost:8000/api/docs/

## Endpoints Principales

La API expone los siguientes endpoints principales:

- `/api/v1/users/register/`: Registro de usuarios
- `/api/v1/auth/login/`: Obtención de tokens JWT
- `/api/v1/users/me/`: Información del usuario autenticado
- `/api/v1/drivers/drivers/`: Gestión de conductores
- `/api/v1/addresses/addresses/`: Gestión de direcciones
- `/api/v1/services/services/`: Gestión de servicios

## Desarrollo Local

### Sin Docker (Entorno virtual)

1. Crear y activar entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements/all.txt
```

3. Configurar variables de entorno y base de datos

4. Ejecutar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

## Test Unitarios

El proyecto incluye una suite completa de pruebas unitarias para garantizar el funcionamiento correcto de todos los componentes. Las pruebas están organizadas por aplicaciones y cubren modelos, serializadores y vistas.

### Ejecución de Tests

Para ejecutar todos los tests:

```bash
python manage.py test
```

Para ejecutar tests específicos de una aplicación:

```bash
python manage.py test apps.users
```

### Cobertura de Tests

Las pruebas cubren:

- Creación y validación de modelos
- Autenticación de usuarios
- Serialización y validación de datos
- Endpoints de API y permisos
- Lógica de negocio específica

#### Ejemplos de Tests Implementados

- **Tests de Modelos**: Validación de campos, relaciones y métodos personalizados.
- **Tests de API**: Verificación de endpoints, permisos y respuestas HTTP.
- **Tests de Serializers**: Validación de datos, creación y actualización de objetos.


## Despliegue en la Nube (AWS/GCP)

### Arquitectura Recomendada en AWS

Para un despliegue escalable y seguro en AWS, se recomienda la siguiente arquitectura:

#### Componentes Principales

1. **Contenedorización con Amazon ECS/Fargate**:
   - Despliegue de la aplicación Django en contenedores sin administrar servidores
   - Auto-escalado basado en demanda
   - Balanceo de carga integrado

2. **Base de Datos con Amazon RDS (PostgreSQL)**:
   - Alta disponibilidad con replicación multi-AZ
   - Copias de seguridad automatizadas
   - Escalado vertical y horizontal según necesidades

3. **Cache con Amazon ElastiCache (Redis)**:
   - Mejora del rendimiento para operaciones frecuentes
   - Almacenamiento de sesiones y resultados de consultas

4. **Balanceo de Carga con Application Load Balancer**:
   - Distribución del tráfico entre múltiples instancias
   - Terminación SSL/TLS
   - Integración con AWS WAF para seguridad adicional

5. **Almacenamiento de Archivos Estáticos con S3**:
   - Alta durabilidad para archivos estáticos y media
   - Integración con CloudFront para CDN

6. **Monitorización y Logging**:
   - CloudWatch para métricas y alertas
   - CloudTrail para auditoría
   - X-Ray para análisis de rendimiento

#### Diagrama Conceptual

```
Internet → CloudFront → ALB → ECS/Fargate → RDS PostgreSQL
                         ↓                  ↓
                        WAF                Redis
                         ↓
                         S3 (Estáticos/Media)
```

#### Implementación con Infraestructura como Código (IaC)

Se recomienda utilizar AWS CDK o Terraform para definir la infraestructura como código, lo que permite:

- Versionado de la infraestructura
- Despliegues repetibles y auditables
- Integración con CI/CD
- Gestión de múltiples entornos (desarrollo, staging, producción)

### Consideraciones de Seguridad

1. **Gestión de Secretos**:
   - Utilizar AWS Secrets Manager para credenciales de base de datos y claves API
   - No almacenar secretos en el código o variables de entorno expuestas

2. **Red y Acceso**:
   - Usar VPC privada para recursos internos
   - Implementar grupos de seguridad restrictivos
   - Uso de bastiones para acceso a instancias

3. **Autenticación y Autorización**:
   - Integración con Amazon Cognito para autenticación de usuarios
   - Implementación de políticas IAM para acceso a recursos AWS
   - Rotación regular de credenciales y tokens

4. **Protección de Datos**:
   - Encriptación en reposo y en tránsito
   - Implementación de políticas de backup
   - Clasificación de datos según sensibilidad

### Escalabilidad

1. **Escalado Horizontal**:
   - Auto-scaling groups para contenedores en ECS
   - Réplicas de lectura para RDS
   - Sharding para bases de datos de gran tamaño

2. **Escalado Vertical**:
   - Ajuste de recursos (CPU, memoria) según demanda
   - Monitorización continua para identificar cuellos de botella

3. **Optimización de Costos**:
   - Uso de instancias reservadas para cargas predecibles
   - Instancias spot para trabajos en segundo plano
   - Implementación de políticas de lifecycle para almacenamiento

### Estrategia de Despliegue Continuo

1. **Pipeline de CI/CD**:
   - AWS CodePipeline o GitHub Actions para automatización
   - Tests automáticos antes del despliegue
   - Estrategia de despliegue Blue/Green para minimizar downtime

2. **Monitorización Post-Despliegue**:
   - Alertas basadas en métricas clave
   - Rollback automatizado ante fallos
   - Dashboards para visualización de estado del sistema

## Contribución

1. Crear una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
2. Hacer commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
3. Hacer push a la rama (`git push origin feature/nueva-caracteristica`)
4. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo MIT.

## Contacto

Telegram - @Mr_3b0y

Enlace del proyecto: [https://github.com/Mr-3b0y/home-delivery-dispatch-api](https://github.com/Mr-3b0y/home-delivery-dispatch-api)