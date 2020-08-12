from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser for convenience with docker compose."

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            admin = User.objects.create_superuser(
                username='admin', password='pass', email='a@a.ru')
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Superuser already exists.')
