from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        if os.environ.get('RUN_ONCE', 'true') == 'true':
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='YourStrongPassword123'
                )