from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from faker import Faker
from decouple import config

from apps.users.models import User
from apps.drivers.models import Driver
from apps.services.models import Service
from apps.addresses.models import Address


class Command(BaseCommand):
    help = 'Load test data into the database'
    
    def handle(self, *args, **kwargs):
        """
        Load test data into the database.
        """
        
        if config('ENV') == 'production':
            self.stdout.write(self.style.ERROR('This command cannot be run in production!'))
            return
        
        
        if User.objects.all().count() >= 20:
            self.stdout.write(self.style.WARNING('Test data already exists.'))
            return
        
        self.stdout.write(self.style.SUCCESS('Starting to load test data...'))
        
        # Create a Faker instance
        fake = Faker()
        self.stdout.write(self.style.NOTICE('Faker instance created'))

        if not User.objects.filter(username='admintest').exists():
            self.stdout.write(self.style.NOTICE('Creating admin user...'))
            super_user = User.objects.create_superuser(
                username='admintest',
                email='admintest@test.co',
                password='AdminTest1234*',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:10],
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {super_user.username}'))

        # Create 20 users
        self.stdout.write(self.style.NOTICE('Creating regular users...'))
        for i in range(20):
            try:
                # Create a valid phone number that matches the RegexValidator pattern (^\+?1?\d{9,15}$)
                phone = '+' + str(fake.random_int(min=1000000000, max=9999999999))
                
                user = User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password='UserTest1234*',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=phone,
                )
                self.stdout.write(self.style.SUCCESS(f'Created user {i+1}/20: {user.username}'))

                # Creating addresses for user
                self.stdout.write(self.style.NOTICE(f'Creating addresses for user {user.username}...'))
                for j in range(3):
                    address = Address.objects.create(
                        street=fake.street_address(),
                        city=fake.city(),
                        state=fake.state(),
                        country=fake.country(),
                        postal_code=fake.postcode(),
                        latitude=fake.coordinate(),
                        longitude=fake.longitude(),
                        created_by=user,
                    )
                    self.stdout.write(self.style.SUCCESS(f'  - Address {j+1}/3 created: {address.street}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating user: {e}"))

        # Create 30 drivers
        self.stdout.write(self.style.NOTICE('Creating drivers...'))
        vehicle_types_brands = [
            'Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan',
            'BMW', 'Mercedes-Benz', 'Volkswagen', 'Hyundai', 'Kia'
        ]
        driver_password='DriverTest1234*'
        for i in range(30):
            phone = '+' + str(fake.random_int(min=1000000000, max=9999999999))
            try:
                driver = Driver(
                    username=fake.user_name(),
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=phone,
                    vehicle_plate=fake.license_plate(),
                    vehicle_model=fake.random_element(elements=vehicle_types_brands),
                    vehicle_color=fake.color_name(),
                    vehicle_year=fake.random_int(min=2000, max=2023),
                    current_latitude=float(fake.latitude()),
                    current_longitude=float(fake.longitude()),
                    is_available=fake.boolean(chance_of_getting_true=70),
                )
                driver.set_password(driver_password)  # Aquí encriptas la contraseña correctamente
                driver.save()

                self.stdout.write(self.style.SUCCESS(f'Created driver {i+1}/30: {driver.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating driver: {e}"))
        
        self.stdout.write(self.style.SUCCESS('Test data loading completed successfully!'))