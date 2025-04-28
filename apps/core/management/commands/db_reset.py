import os
import glob
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Elimina todas las tablas de la base de datos y los archivos de migración (¡CUIDADO!)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("¡Este comando eliminará todas las tablas de la base de datos y los archivos de migración!"))
        confirm = input("¿Estás seguro? (y/n): ")

        if confirm.lower() != 'y':
            self.stdout.write(self.style.ERROR("Operación cancelada."))
            return

        # Eliminar todas las tablas de la base de datos
        with connection.cursor() as cursor:
            # Desactivar claves foráneas temporalmente
            if connection.vendor == 'sqlite':
                cursor.execute("PRAGMA foreign_keys = OFF;")
            elif connection.vendor == 'mysql':
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            elif connection.vendor == 'postgresql':
                cursor.execute("SET session_replication_role = replica;")

            # Obtener todas las tablas
            tables = connection.introspection.table_names()
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                self.stdout.write(f'Tabla eliminada: {table}')

            # Reactivar claves foráneas
            if connection.vendor == 'sqlite':
                cursor.execute("PRAGMA foreign_keys = ON;")
            elif connection.vendor == 'mysql':
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            elif connection.vendor == 'postgresql':
                cursor.execute("SET session_replication_role = origin;")

        self.stdout.write(self.style.SUCCESS("¡Todas las tablas han sido eliminadas!"))

        # Eliminar archivos de migración
        self.stdout.write(self.style.WARNING("Eliminando archivos de migración..."))
        for app_config in apps.get_app_configs():
            migrations_path = os.path.join(app_config.path, 'migrations')
            if os.path.exists(migrations_path):
                migration_files = glob.glob(os.path.join(migrations_path, '*.py'))
                for migration_file in migration_files:
                    if os.path.basename(migration_file) != '__init__.py':  # No eliminar __init__.py
                        os.remove(migration_file)
                        self.stdout.write(f'Archivo de migración eliminado: {migration_file}')
        self.stdout.write(self.style.SUCCESS("¡Todos los archivos de migración han sido eliminados!"))
